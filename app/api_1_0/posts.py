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


@api.route("/post/<int:post_id>", methods=["PUT"])
def edit_post(post_id):
    return BLPost.edit_post(request, post_id)


@api.route("/post/<int:post_id>", methods=["DELETE"])
def DELETE_post(post_id):
    return BLPost.delete_post(post_id)
