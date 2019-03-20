from .. import db
from .PostSubject import PostSubject


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    name = db.Column(db.String(64), unique=True)

    parent = db.relationship("Subject", backref="children", remote_side=[id])
    posts = db.relationship("PostSubject",
                            foreign_keys=[PostSubject.post_id, PostSubject.subject_id],
                            backref=db.backref("post", lazy="joined"),
                            lazy="dynamic",
                            cascade="all, delete-orphan")

    def __repr__(self):
        return "<Subject %r>" % self.name

    def to_json(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "name": self.name
        }
