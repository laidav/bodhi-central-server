from . import api
from ..database import Practice
from flask import g, jsonify, request


@api.route("/practice")
def get_practices():

    post_id = request.args.get("post_id")

    practices = Practice.query.filter_by(author=g.current_user)

    if post_id:
        practices.filter_by(post_id=post_id)

    practices = practices.all()

    return jsonify({
        "practices": [practice.to_json() for practice in practices]
    })

