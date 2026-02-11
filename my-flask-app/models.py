from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        # เมื่อมีการเซ็ตค่า password ให้แปลงเป็น Hash ทันที
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # ฟังก์ชันเช็ค password
        return check_password_hash(self.password_hash, password)
