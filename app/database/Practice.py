from .. import db
from datetime import datetime


class Practice(db.Model):
    __tablename__ = "practices"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    dukkha_id = db.Column(db.Integer, db.ForeignKey("dukkhas.id"))
    title = db.Column(db.String(250))
    notes = db.Column(db.Text)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Practice %r>" % self.title

    def to_json(self):
        return {
            "id": self.id,
            "subject": self.subject.to_json(),
            "dukkha": self.dukkha.to_json(),
            "title": self.title,
            "notes": self.notes,
            "created_date": self.created_date
        }
