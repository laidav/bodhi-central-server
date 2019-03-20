from .. import db


class PostSubject(db.Model):
    __tablename__ = "postsubject"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), primary_key=True)

    def __repr__(self):
        return "<PostSubject %r, %r>" % (self.post_id, self.subject_id)
