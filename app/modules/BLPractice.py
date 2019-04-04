from ..db_models import Practice, Post, Subject, PracticeSubject
from flask import g, jsonify
from .. import db
from .schemas.practice_schema import PracticeSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError, SubjectNotFoundError, PracticeNotFoundError


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

            result = jsonify(new_practice.created_to_json()), ErrorCodes.HTTP_STATUS_CREATED
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

    @classmethod
    def edit_practice(cls, request, practice_id):
        data = request.json

        try:
            practice = Practice.query.get(practice_id)

            if practice is None:
                raise PracticeNotFoundError

            data = cls.__validate_data(data)
            new_subjects = data["subjects"] if data["subjects"] is not None else []

            current_subjects = [practice_subject.subject_id for practice_subject in PracticeSubject.query.filter_by(
                practice_id=practice.id)]

            subjects_to_add = [PracticeSubject(practice_id=practice_id,
                                               subject_id=subject_id)
                               for subject_id in new_subjects if subject_id not in current_subjects]

            subjects_to_delete = [subject_id for subject_id in current_subjects if subject_id not in new_subjects]

            del data["subjects"]

            practice.update_from_json(data)

            add_params = subjects_to_add + [practice]

            db.session.add_all(add_params)

            for subject_id in subjects_to_delete:
                PracticeSubject.query.filter(PracticeSubject.practice_id == practice_id,
                                             PracticeSubject.subject_id == subject_id).delete()

            db.session.commit()

            result = jsonify({"error": ErrorCodes.SUCCESS}), ErrorCodes.HTTP_STATUS_SUCCESS
        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
                     ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except PostNotFoundError as e:
            result = jsonify({"error": e.error}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND
        except SubjectNotFoundError as e:
            result = jsonify({"error": e.error}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND
        except PracticeNotFoundError as e:
            result = jsonify({"error": e.error}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @staticmethod
    def __validate_data(data):
        data = PracticeSchema.validate(data)
        subjects = data["subjects"] if data["subjects"] is not None else []

        data["post_id"] = data.get("post_id")

        post = None if data["post_id"] is None else Post.query.get(data["post_id"])

        if data["post_id"] is not None and post is None:
            raise PostNotFoundError

        for subject_id in subjects:
            if db.session.query(Subject.id).filter_by(id=subject_id).scalar() is None:
                raise SubjectNotFoundError

        return data
