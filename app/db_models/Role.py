from .. import db


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship("User", backref="role")

    def __repr__(self):
        return "<Role %r>" % self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
