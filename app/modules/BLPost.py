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

    @staticmethod
    def get_single_post(post_id):
        try:
            post = Post.query.get(post_id)

            if post is None:
                raise PostNotFoundError

            result = jsonify(post.to_json()), ErrorCodes.HTTP_STATUS_SUCCESS

        except PostNotFoundError as e:
            result = jsonify({"error": e.error}), ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @classmethod
    def add_post(cls, request):
        try:
            data = cls.__validate_data(request.json)
            subjects = data["subjects"]

            del data["subjects"]

            new_post = Post(data)
            new_post.author = g.current_user

            params = [new_post]

            for subject_id in subjects:
                params.append(PostSubject(post=new_post, subject_id=subject_id))

            db.session.add_all(params)
            db.session.commit()

            result = jsonify(new_post.to_json()), ErrorCodes.HTTP_STATUS_CREATED

        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
                     ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except SubjectNotFoundError as e:
            result = jsonify({"error": ErrorCodes.SUBJECT_NOT_FOUND}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @staticmethod
    def __validate_data(data):
        data = PostSchema.validate(data)

        subjects = data["subjects"]

        data["post_id"] = data.get("post_id")

        for subject_id in subjects:
            if db.session.query(Subject.id).filter_by(id=subject_id).scalar() is None:
                raise SubjectNotFoundError

        return data
