from . import api
from ..modules.BCPost import BCPost
from flask import request
from .authentication import auth


@api.route("/post", methods=["GET"])
@auth.login_required
def get_posts():
    return BCPost.get_posts(request)


@api.route("/post/<int:post_id>", methods=["GET"])
@auth.login_required
def get_post(post_id):
    return BCPost.get_single_post(post_id)


@api.route("/post", methods=["POST"])
@auth.login_required
def add_post():
    return BCPost.add_post(request)


@api.route("/post/<int:post_id>", methods=["PUT"])
@auth.login_required
def edit_post(post_id):
    return BCPost.edit_post(request, post_id)


@api.route("/post/<int:post_id>", methods=["DELETE"])
@auth.login_required
def DELETE_post(post_id):
    return BCPost.delete_post(post_id)
