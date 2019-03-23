from .. import db
from datetime import datetime


class Practice(db.Model):
    __tablename__ = "practices"

    id = db.Column(db.Integer, primary_key=True)
    teaching_point = db.Column(db.String(250))
    application = db.Column(db.Text)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def __repr__(self):
        return "<Practice %r>" % self.teaching_point

    def to_json(self):
        return {
            "id": self.id,
            "teaching_point": self.teaching_point,
            "application": self.application,
            "created": self.created,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
