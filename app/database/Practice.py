from .. import db
from datetime import datetime
from .PracticeSubject import PracticeSubject
from ..exceptions import ValidationError


class Practice(db.Model):
    __tablename__ = "practices"

    id = db.Column(db.Integer, primary_key=True)
    teaching_point = db.Column(db.String(250))
    application = db.Column(db.Text)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    subjects = db.relationship("PracticeSubject",
                               foreign_keys=[PracticeSubject.subject_id, PracticeSubject.practice_id],
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

    @staticmethod
    def from_json(json_post):
        teaching_point = json_post.get("teaching_point")
        application = json_post.get("application")
        if teaching_point is None or teaching_point == "":
            raise ValidationError("post does not have a body")

        return Practice(teaching_point=teaching_point, application=application)


