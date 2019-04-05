from . import api
from ..modules.BLPost import BLPost
from flask import jsonify


@api.route("/post")
def get_posts():
    return BLPost.get_posts()


@api.route("/post/<int:post_id>")
def get_post(post_id):
    return BLPost.get_single_post(post_id)
