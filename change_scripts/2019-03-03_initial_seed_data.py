import os
import sys

sys.path.append('..')

from config import config
from flask import Flask
from app.database import User, Role, Dukkha, Subject, Practice
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config[os.getenv("FLASK_CONFIG") or "default"])

db = SQLAlchemy()

db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        admin_role = Role(name="Administrator")
        mod_role = Role(name="Moderator")
        user_role = Role(name="User")
        user_david = User(username="Dave", role=admin_role, email="laidav@gmail.com", confirmed=True)
        user_david.password = "Password1!"
        dukkha = Dukkha(title="First Dukkha!", description="Dukkha description!", author=user_david)
        wisdom = Subject(name="Wisdom")
        ethics = Subject(name="Ethics")
        meditation = Subject(name="Meditation")
        right_view = Subject(name="Right View", parent=wisdom)
        right_intention = Subject(name="Right Intention", parent=wisdom)
        practice = Practice(title="First Practice", notes="First notes in practice!", subject=right_view, dukkha=dukkha)

        db.session.add_all([admin_role, mod_role, user_role, user_david, dukkha, wisdom,
                            ethics, meditation, right_view, right_intention, practice])

        db.session.commit()

        print("Seed data initialized!")
