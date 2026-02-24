import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

STATUS = [
    ("active", "Active"),
    ("disactive", "Disactive"),
]
USER_ROLES = [
    ("admin", "Admin"),
    ("user", "User"),
]


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256))
    password_hash = db.Column(db.String(255))

    status = db.Column(db.String(50), nullable=False, default="active")
    roles = db.Column(db.JSON, default=lambda: ["user"])

    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_roles(self, roles_to_check):
        if not self.roles:
            return False
        for role in roles_to_check:
            if role in self.roles:
                return True
        return False
