from .. import db


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    name = db.Column(db.String(64), unique=True)

    parent = db.relationship('Subject', backref='children', remote_side=[id])

    def __repr__(self):
        return '<Subject %r>' % self.name
