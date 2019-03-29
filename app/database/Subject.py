from .. import db
from .PostSubject import PostSubject


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    first_child_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), unique=True)
    right_sibling_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), unique=True)
    name = db.Column(db.String(64), unique=True)

    first_child = db.relationship("Subject", backref="parent",
                                  remote_side=[id],
                                  uselist=False,
                                  foreign_keys=first_child_id)
    right_sibling = db.relationship("Subject", backref="left_sibling",
                                    remote_side=[id],
                                    uselist=False,
                                    foreign_keys=right_sibling_id)

    post_subjects = db.relationship("PostSubject",
                                    foreign_keys=[PostSubject.post_id, PostSubject.subject_id],
                                    backref=db.backref("subject", lazy="joined"),
                                    lazy="dynamic",
                                    cascade="all, delete-orphan")

    def __repr__(self):
        return "<Subject %r>" % self.name

    def to_json(self):
        return {
            "id": self.id,
            "first_child_id": self.first_child_id,
            "right_sibling_id": self.right_sibling_id,
            "name": self.name
        }
