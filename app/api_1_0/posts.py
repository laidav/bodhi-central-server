from . import api
from ..database import Post, Practice
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

    practices = Practice.query.filter_by(post_id=post_id, author=g.current_user)

    practices_json = {
        "practices": [practice.to_json() for practice in practices]
    }

    post.update(practices_json)

    return jsonify(post)
