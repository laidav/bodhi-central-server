import os
import sys

sys.path.append('..')

from config import config
from flask import Flask
from app.db_models import User, Role, Post, Subject, PostSubject, Practice, PracticeSubject
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

        buddha = Subject(name="Buddha")
        wisdom = Subject(name="Wisdom")
        ethics = Subject(name="Ethics")
        meditation = Subject(name="Meditation")

        buddha.first_child = wisdom
        wisdom.right_sibling = ethics
        ethics.right_sibling = meditation

        right_view = Subject(name="Right View")
        right_intention = Subject(name="Right Intention")

        wisdom.first_child = right_view
        right_view.right_sibling = right_intention

        right_speech = Subject(name="Right Speech")
        right_action = Subject(name="Right Action")
        right_livelihood = Subject(name="Right Livelihood")

        ethics.first_child = right_speech
        right_speech.right_sibling = right_action
        right_action.right_sibling = right_livelihood

        right_effort = Subject(name="Right Effort")
        right_mindfulness = Subject(name="Right Mindfulness")
        right_concentration = Subject(name="Right Concentration")

        meditation.first_child = right_effort
        right_effort.right_sibling = right_mindfulness
        right_mindfulness.right_sibling = right_concentration

        post = Post(title="Ajahn Chah: The Peace Beyond",
                    description="Ajahn Chah gives talk on the birth and death of suffering",
                    link="https://www.youtube.com/watch?v=Mtqz82w4v0s",
                    author=user_david)

        post_2 = Post(title="Ajahn Chah: No Abiding",
                      description="Ajahn Chah gives talk on permenance and the beauty of being empty",
                      link="https://www.youtube.com/watch?v=b5vltJm9UrM&t=116s",
                      author=user_david)

        post_subject_a = PostSubject(post=post, subject=right_view)
        post_subject_b = PostSubject(post=post, subject=right_intention)

        post_2_subject_a = PostSubject(post=post_2, subject=right_view)
        post_2_subject_b = PostSubject(post=post_2, subject=right_intention)

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
                              post=post_2)
        
        practice_subject_a = PracticeSubject(practice=practice, subject=right_view)
        practice_subject_b = PracticeSubject(practice=practice, subject=meditation)

        practice_2_subject_a = PracticeSubject(practice=practice_2, subject=right_view)
        practice_2_subject_b = PracticeSubject(practice=practice_2, subject=meditation)

        db.session.add_all([admin_role, mod_role, user_role, user_david, buddha, wisdom,
                            ethics, meditation, right_view, right_intention, right_speech,
                            right_action, right_livelihood, right_effort, right_mindfulness,
                            right_concentration, post, post_2, post_subject_a, post_subject_b, practice,
                            practice_2, practice_subject_a, practice_subject_b, practice_2_subject_a,
                            practice_2_subject_b])

        db.session.commit()

        print("Seed data initialized!")
