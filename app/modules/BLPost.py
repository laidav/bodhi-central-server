from ..db_models import Post, Subject, PostSubject
from flask import g, jsonify
from .. import db
from .schemas.post_schema import PostSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError, SubjectNotFoundError


class BLPost:
    @staticmethod
    def get_posts():
        posts = Post.query.all()
        result = jsonify({"posts": [practice.to_json() for practice in posts]}), ErrorCodes.HTTP_STATUS_SUCCESS

        return result

    @classmethod
    def get_single_post(cls, post_id):
        try:
            post = Post.query.get(post_id)

            if post is None:
                raise PostNotFoundError

            result = jsonify(post.to_json()), ErrorCodes.HTTP_STATUS_SUCCESS

        except PostNotFoundError as e:
            result = jsonify({"error": e.error}), ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    # @staticmethod
    # def __validate_data(data):
    #     data = PostSchema.validate(data)
    #     subjects = data["subjects"] if data["subjects"] is not None else []
    #
    #     data["post_id"] = data.get("post_id")
    #
    #     post = None if data["post_id"] is None else Post.query.get(data["post_id"])
    #
    #     if data["post_id"] is not None and post is None:
    #         raise PostNotFoundError
    #
    #     for subject_id in subjects:
    #         if db.session.query(Subject.id).filter_by(id=subject_id).scalar() is None:
    #             raise SubjectNotFoundError
    #
    #     return data
