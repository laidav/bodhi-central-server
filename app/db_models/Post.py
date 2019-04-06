from .. import db
from datetime import datetime
from .PostSubject import PostSubject
from ..modules.BLDecorators import set_attributes_decorator, update_from_json_decorator


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text)
    link = db.Column(db.String(250))
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    subjects = db.relationship("PostSubject",
                               foreign_keys=[PostSubject.subject_id, PostSubject.post_id],
                               backref=db.backref("post", lazy="joined"),
                               lazy="dynamic",
                               cascade="all, delete-orphan")

    practices = db.relationship("Practice", backref="post")

    def __repr__(self):
        return "<Post %r>" % self.title

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "created": self.created,
            "subjects": [subject.subject.to_json() for subject in self.subjects],
            "author": self.author.to_json()
        }

    @update_from_json_decorator
    def update_from_json(self, data):
        pass

    @set_attributes_decorator
    def __init__(self, *initial_data, **kwargs):
        pass
