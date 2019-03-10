from .. import db
from datetime import datetime


class Dukkha(db.Model):
    __tablename__ = 'dukkhas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    teachings = db.relationship('Teaching', backref='dukkha')

    def __repr__(self):
        return '<Dukkha %r>' % self.title
