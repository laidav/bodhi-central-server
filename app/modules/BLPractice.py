from ..database import Practice
from flask import g, jsonify
from .. import db


class BLPractice:
    @classmethod
    def get_practices(cls, post_id):
        practices = Practice.query.filter_by(author=g.current_user)

        if post_id:
            practices.filter_by(post_id=post_id)

        practices = practices.all()

        return jsonify({
            "practices": [practice.to_json() for practice in practices]
        })

    @staticmethod
    def add_practice(request):
        new_practice = Practice.from_json(request.json)
        new_practice.author = g.current_user
        db.session.add(new_practice)
        db.session.commit()

        return jsonify(new_practice.to_json()), 201

