from .. import db
from datetime import datetime


class Teaching(db.Model):
    __tablename__ = 'teachings'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    dukkha_id = db.Column(db.Integer, db.ForeignKey('dukkhas.id'))
    title = db.Column(db.String(250))
    notes = db.Column(db.Text)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Teaching %r>' % self.title
