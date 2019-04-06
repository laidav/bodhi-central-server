from . import api
from ..modules.BLPost import BLPost
from flask import request


@api.route("/post", methods=["GET"])
def get_posts():
    return BLPost.get_posts()


@api.route("/post/<int:post_id>", methods=["GET"])
def get_post(post_id):
    return BLPost.get_single_post(post_id)


@api.route("/post", methods=["POST"])
def add_post():
    return BLPost.add_post(request)
