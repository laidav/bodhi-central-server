from .. import db


class PracticeSubject(db.Model):
    __tablename__ = "practice_subject"

    practice_id = db.Column(db.Integer, db.ForeignKey("practices.id"), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), primary_key=True)

    def __repr__(self):
        return "<PracticeSubject %r, %r>" % (self.practice_id, self.subject_id)
