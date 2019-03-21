import os
import sys

sys.path.append('..')

from config import config
from flask import Flask
from app.database import User, Role, Post, Subject, PostSubject
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
        user_david = User(username="Dave",
                          role=admin_role,
                          email="laidav@gmail.com",
                          confirmed=True)
        user_david.password = "Password1!"
        wisdom = Subject(name="Wisdom")
        ethics = Subject(name="Ethics")
        meditation = Subject(name="Meditation")
        right_view = Subject(name="Right View", parent=wisdom)
        right_intention = Subject(name="Right Intention", parent=wisdom)
        post = Post(title="First Post",
                    description="First Post Description!",
                    link="www.somearticle.com",
                    author=user_david)

        post_subject_a = PostSubject(post=post, subject=right_view)
        post_subject_b = PostSubject(post=post, subject=right_intention)

        db.session.add_all([admin_role, mod_role, user_role, user_david, wisdom,
                            ethics, meditation, right_view, right_intention, post,
                            post_subject_a, post_subject_b])

        db.session.commit()

        print("Seed data initialized!")
