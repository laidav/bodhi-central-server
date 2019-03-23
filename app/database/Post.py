from .. import db
from datetime import datetime
from .PostSubject import PostSubject
from sqlalchemy.ext.associationproxy import association_proxy


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

    subject_ids = association_proxy("postsubject", "subject_id")

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
            "subjects": self.subject_ids
        }
