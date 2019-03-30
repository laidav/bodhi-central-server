from . import api
from flask import request
from ..modules import BLPractice


@api.route("/practice")
def get_practices():

    post_id = request.args.get("post_id")

    practices = BLPractice.get_practices(post_id)

    return practices

