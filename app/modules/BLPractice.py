from ..database import Practice, Post
from flask import g, jsonify
from .. import db
from .schemas.practice_schema import AddPracticeSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError


class BLPractice:
    @classmethod
    def get_practices(cls, post_id):
        practices = Practice.query.filter_by(author=g.current_user)

        if post_id:
            practices.filter_by(post_id=post_id)

        practices = practices.all()

        return jsonify({
            "practices": [practice.to_json() for practice in practices]
        })

    @staticmethod
    def add_practice(request):
        try:
            new_practice = request.json
            new_practice = AddPracticeSchema.validate(new_practice)
            new_practice = Practice.from_json(new_practice)

            post = None if new_practice.post_id is None else Post.query.get(new_practice.post_id)

            if new_practice.post_id is not None and post is None:
                raise PostNotFoundError

            new_practice.post = post

            new_practice.author = g.current_user
            db.session.add(new_practice)
            db.session.commit()

            error_code = ErrorCodes.ERROR_SUCCESS
        except SchemaError:
            error_code = ErrorCodes.ERROR_SCHEMA_VALIDATION
        except PostNotFoundError:
            error_code = ErrorCodes.POST_NOT_FOUND

        if error_code == ErrorCodes.ERROR_SUCCESS:
            return jsonify(new_practice.created_to_json()), ErrorCodes.HTTP_CREATED

        return jsonify({"error": error_code}), ErrorCodes.HTTP_BAD_REQUEST


