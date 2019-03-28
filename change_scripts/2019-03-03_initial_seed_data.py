import os
import sys

sys.path.append('..')

from config import config
from flask import Flask
from app.database import User, Role, Post, Subject, PostSubject, Practice
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
        post = Post(title="Ajahn Chah: The Peace Beyond",
                    description="Ajahn Chah gives talk on the birth and death of suffering",
                    link="https://www.youtube.com/watch?v=Mtqz82w4v0s",
                    author=user_david)

        post_subject_a = PostSubject(post=post, subject=right_view)
        post_subject_b = PostSubject(post=post, subject=right_intention)

        practice = Practice(teaching_point="Happiness and Unhappiness are "
                                           "equal in disturbing peace and enlightment."
                                           "Meditation helps us not cling on to these things",
                            application="Rifle Shooting - Clinging on to a good shot or bad shot"
                                        "distracts you out of the moment, preventing you from doing what you"
                                        "need to do.",
                            author=user_david,
                            post=post)

        practice_2 = Practice(teaching_point="We hold and let go, but we do not cling.  We hold "
                                             "onto things all the time, but we don't cling.",
                              application="While meditating during breath, I tried holding on"
                                          "in breath and letting go on out breath.  I am not 'clinging"
                                          "on' to 'letting go'.  The breath is so beautiful, maybe life is"
                                          "all about holding and letting go, just like the breath",
                              author=user_david,
                              post=post)

        db.session.add_all([admin_role, mod_role, user_role, user_david, wisdom,
                            ethics, meditation, right_view, right_intention, post,
                            post_subject_a, post_subject_b, practice, practice_2])

        db.session.commit()

        print("Seed data initialized!")
