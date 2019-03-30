from ..database import Practice
from flask import g, jsonify


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
