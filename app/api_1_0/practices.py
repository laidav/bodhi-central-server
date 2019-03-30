from . import api
from flask import request
from ..modules import BLPractice


@api.route("/practice", methods=["GET"])
def get_practices():

    post_id = request.args.get("post_id")

    practices = BLPractice.get_practices(post_id)

    return practices


@api.route("/practice", methods=["POST"])
def add_practice():
    new_practice = BLPractice.add_practice(request)

    return new_practice



