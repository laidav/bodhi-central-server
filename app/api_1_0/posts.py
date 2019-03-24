from . import api
from ..database import Post
from flask import g, jsonify


@api.route("/post")
def get_posts():

    posts = Post.query.all()

    return jsonify({
        "posts": [post.to_json() for post in posts]
    })


@api.route("/post/<int:post_id>")
def get_post(post_id):
    post = Post.query.get_or_404(post_id).to_json()

    return jsonify(post)
