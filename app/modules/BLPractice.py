from ..database import Practice, Post, Subject, PracticeSubject
from flask import g, jsonify
from .. import db
from .schemas.practice_schema import AddPracticeSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError, SubjectNotFoundError


class BLPractice:
    @staticmethod
    def get_practices(post_id):
        practices = Practice.query.filter_by(author=g.current_user)

        if post_id:
            practices.filter_by(post_id=post_id)

        practices = practices.all()

        return jsonify({
            "practices": [practice.to_json() for practice in practices]
        })

    @staticmethod
    def add_practice(request):
        new_practice = request.json

        try:
            new_practice = AddPracticeSchema.validate(new_practice)
            subjects = new_practice["subjects"] if new_practice["subjects"] is not None else []
            del new_practice["subjects"]
            new_practice = Practice.from_json(new_practice)
            new_practice.author = g.current_user

            params = [new_practice]

            post = None if new_practice.post_id is None else Post.query.get(new_practice.post_id)

            if new_practice.post_id is not None and post is None:
                raise PostNotFoundError

            for subject_id in subjects:
                exists = db.session.query(Subject.id).filter_by(id=subject_id).scalar()
                if exists is None:
                    raise SubjectNotFoundError

                params.append(PracticeSubject(practice=new_practice,
                                              subject_id=subject_id))

            db.session.add_all(params)
            db.session.commit()

            error_code = ErrorCodes.ERROR_SUCCESS
        except SchemaError:
            error_code = ErrorCodes.ERROR_SCHEMA_VALIDATION
        except PostNotFoundError as e:
            error_code = e.error
        except SubjectNotFoundError as e:
            error_code = e.error

        if error_code == ErrorCodes.ERROR_SUCCESS:
            return jsonify(new_practice.created_to_json()), ErrorCodes.HTTP_CREATED

        return jsonify({"error": error_code}), ErrorCodes.HTTP_BAD_REQUEST


