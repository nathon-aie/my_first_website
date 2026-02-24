#!/usr/bin/env python
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import db, User


def init_admin():
    """Initialize admin user"""
    with app.app_context():
        print("=" * 50)
        print("Admin User Initialization")
        print("=" * 50)

        # Check if admin user already exists
        admin_user = User.query.filter_by(username="admin").first()
        if admin_user:
            print("Admin user already exists!")
            return

        # Set default values
        username = "admin"
        email = "admin@gmail.com"
        password = "123456"

        # Create admin user
        admin_user = User(
            username=username, email=email, status="active", roles=["admin", "user"]
        )
        admin_user.password = password

        try:
            db.session.add(admin_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {str(e)}")


if __name__ == "__main__":
    init_admin()
