import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from models import db, User
import views

import acl

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    acl.init_acl(app)

    @acl.login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    views.register_blueprint(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
