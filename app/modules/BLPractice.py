from ..database import Practice, Post, Subject, PracticeSubject
from flask import g, jsonify
from .. import db
from .schemas.practice_schema import AddPracticeSchema, EditPracticeSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError, SubjectNotFoundError


class BLPractice:
    @staticmethod
    def get_practices(request):
        practices = Practice.query.filter_by(author=g.current_user)

        post_id = request.args.get("post_id")

        if post_id:
            practices.filter_by(post_id=post_id)

        practices = practices.all()

        return jsonify({
            "practices": [practice.to_json() for practice in practices]
        })

    @classmethod
    def add_practice(cls, request):
        data = request.json

        try:
            data = cls.__validate_data(data)
            subjects = data["subjects"] if data["subjects"] is not None else []

            del data["subjects"]

            new_practice = Practice.from_json(data)
            new_practice.author = g.current_user

            params = [new_practice]

            for subject_id in subjects:
                params.append(PracticeSubject(practice=new_practice,
                                              subject_id=subject_id))

            db.session.add_all(params)
            db.session.commit()

            result = jsonify({"error": ErrorCodes.SUCCESS}), ErrorCodes.HTTP_STATUS_CREATED
        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
                     ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except PostNotFoundError as e:
            result = jsonify({"error": e.error}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND
        except SubjectNotFoundError as e:
            result = jsonify({"error": e.error}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    # @classmethod
    # def edit_practice(cls, request):
    #     data = request.json
    #
    #     try:
    #         data = cls.__validate_data(data)
    #         subjects = data["subjects"] if data["subjects"] is not None else []
    #
    #         del data["subjects"]
    #
    #         new_practice = Practice.from_json(data)
    #         new_practice.author = g.current_user
    #
    #         params = [new_practice]
    #
    #         for subject_id in subjects:
    #             params.append(PracticeSubject(practice=new_practice,
    #                                           subject_id=subject_id))
    #
    #         db.session.add_all(params)
    #         db.session.commit()
    #
    #         result = jsonify({"error": ErrorCodes.SUCCESS}), ErrorCodes.HTTP_STATUS_CREATED
    #     except SchemaError:
    #         result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
    #                  ErrorCodes.HTTP_STATUS_BAD_REQUEST
    #     except PostNotFoundError as e:
    #         result = jsonify({"error": e.error}), \
    #                  ErrorCodes.HTTP_STATUS_NOT_FOUND
    #     except SubjectNotFoundError as e:
    #         result = jsonify({"error": e.error}), \
    #                  ErrorCodes.HTTP_STATUS_NOT_FOUND
    #
    #     return result

    @staticmethod
    def __validate_data(data):
        data = AddPracticeSchema.validate(data)
        subjects = data["subjects"] if data["subjects"] is not None else []
        post = None if data["post_id"] is None else Post.query.get(data["post_id"])

        if data["post_id"] is not None and post is None:
            raise PostNotFoundError

        for subject_id in subjects:
            if db.session.query(Subject.id).filter_by(id=subject_id).scalar() is None:
                raise SubjectNotFoundError

        return data
