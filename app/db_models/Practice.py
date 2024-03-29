from .. import db
from datetime import datetime
from .PracticeSubject import PracticeSubject
from ..modules.BCDecorators import set_attributes_decorator, update_from_json_decorator


class Practice(db.Model):
    __tablename__ = "practices"

    id = db.Column(db.Integer, primary_key=True)
    teaching_point = db.Column(db.Text)
    application = db.Column(db.Text)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    subjects = db.relationship("PracticeSubject",
                               foreign_keys=[
                                   PracticeSubject.subject_id, PracticeSubject.practice_id],
                               backref=db.backref("practice", lazy="joined"),
                               lazy="dynamic",
                               cascade="all, delete-orphan")

    def __repr__(self):
        return "<Practice %r>" % self.teaching_point

    def to_json(self):
        return {
            "id": self.id,
            "teaching_point": self.teaching_point,
            "application": self.application,
            "created": self.created,
            "author_id": self.author_id,
            "subjects": [subject.subject.to_json() for subject in self.subjects],
            "post": self.post.to_json() if self.post is not None else None
        }

    @update_from_json_decorator
    def update_from_json(self, data):
        pass

    @set_attributes_decorator
    def __init__(self, *initial_data, **kwargs):
        pass
