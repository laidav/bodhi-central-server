from .. import db


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Topic %r>" % self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
