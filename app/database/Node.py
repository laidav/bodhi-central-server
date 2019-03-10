from .. import db


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    name = db.Column(db.String(64), unique=True)

    parent = db.relationship('Node', backref='children', remote_side=[id])

    def __repr__(self):
        return '<Node %r>' % self.name
