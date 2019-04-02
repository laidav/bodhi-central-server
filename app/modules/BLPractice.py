from ..database import Practice, Post, Subject, PracticeSubject
from flask import g, jsonify
from .. import db
from .schemas.practice_schema import AddPracticeSchema
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


