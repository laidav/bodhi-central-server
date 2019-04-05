from ..db_models import Post, Subject, PostSubject
from flask import g, jsonify
from .. import db
from .schemas.post_schema import PostSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError, SubjectNotFoundError, PracticeNotFoundError


class BLPost:
    @staticmethod
    def get_posts():
        posts = Post.query.all()

        return jsonify({
            "posts": [post.to_json() for post in posts]
        })

    @classmethod
    def get_single_post(cls, post_id):
        post = Post.query.get(post_id).to_json()
        return jsonify(post)

    @staticmethod
    def __validate_data(data):
        data = PostSchema.validate(data)
        subjects = data["subjects"] if data["subjects"] is not None else []

        data["post_id"] = data.get("post_id")

        post = None if data["post_id"] is None else Post.query.get(data["post_id"])

        if data["post_id"] is not None and post is None:
            raise PostNotFoundError

        for subject_id in subjects:
            if db.session.query(Subject.id).filter_by(id=subject_id).scalar() is None:
                raise SubjectNotFoundError

        return data
