from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User
from forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        # เช็คว่ามี user นี้หรือยัง
        if User.query.filter_by(username=form.username.data).first():
            flash("Username นี้ถูกใช้ไปแล้ว", "error")
            return redirect(url_for("auth.register"))
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.password = form.password.data  # Trigger @password.setter ใน models.py

        db.session.add(new_user)
        db.session.commit()

        flash("สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # ใช้ verify_password จาก models.py
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash("ยินดีต้อนรับกลับ!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ออกจากระบบแล้ว", "info")
    return redirect(url_for("main.index"))
