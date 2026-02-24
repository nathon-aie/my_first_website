from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User, USER_ROLES
from forms import EditRoleForm, LoginForm, RegisterForm
import acl

module = Blueprint("accounts", __name__, url_prefix="/accounts")


@module.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        # เช็คว่ามี user นี้หรือยัง
        if User.query.filter_by(username=form.username.data).first():
            flash("Username นี้ถูกใช้ไปแล้ว", "error")
            return redirect(url_for("accounts.register"))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.password = form.password.data  # Trigger @password.setter ใน models.py

        db.session.add(new_user)
        db.session.commit()

        flash("สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ", "success")
        return redirect(url_for("accounts.login"))

    return render_template("accounts/register.html", form=form)


@module.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash("ยินดีต้อนรับกลับ!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "error")

    return render_template("accounts/login.html", form=form)


@module.route("/users")
@login_required
def users():
    all_users = User.query.all()
    return render_template("accounts/users.html", users=all_users)


@module.route("/edit_roles/<int:user_id>", methods=["GET", "POST"])
@login_required
@acl.roles_required("admin")
def edit_roles(user_id):
    user = User.query.get_or_404(user_id)
    form = EditRoleForm()

    form.roles.choices = USER_ROLES

    if request.method == "GET":
        form.roles.data = user.roles or []

    if form.validate_on_submit():
        # 3. form.roles.data ที่ส่งกลับมาจะเป็น List ของ String ที่ผู้ใช้เลือก
        user.roles = form.roles.data

        db.session.commit()
        flash("อัปเดตสิทธิ์เรียบร้อย", "success")
        return redirect(url_for("accounts.users"))

    return render_template("accounts/edit_roles.html", user=user, form=form)


@module.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ออกจากระบบแล้ว", "info")
    return redirect(url_for("main.index"))
