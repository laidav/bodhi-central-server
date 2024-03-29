from ..db_models import Practice, Post, Subject, PracticeSubject
from flask import g, jsonify, current_app
from .. import db
from .schemas.practice_schema import PracticeSchema, GetPracticesSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError, SubjectNotFoundError, PracticeNotFoundError
from .BCTree import BCTree


class BCPractice:
    @staticmethod
    def get_practices(request):
        try:
            filters = GetPracticesSchema.validate(
                request.args.to_dict(flat=False))

            subjects = set()
            practice_subjects = []
            practices = Practice.query.filter_by(
                author=g.current_user).order_by(db.desc(Practice.created))

            if "post_id" in filters:
                practices = practices.filter(
                    Practice.post_id == filters["post_id"])

            if "subject_id[]" in filters:
                for subject_id in filters["subject_id[]"]:
                    subject = Subject.query.get(subject_id)

                    if subject is not None:
                        subjects = subjects | set(BCTree.get_descendants(subject)) \
                            if subject_id not in subjects else set()
                    else:
                        subjects = subjects | subject_id

                if len(subjects):
                    practice_subjects = PracticeSubject.query.filter(PracticeSubject.subject_id.in_(subjects)).order_by(
                        PracticeSubject.practice_id).with_entities(PracticeSubject.practice_id).all()

                    practice_subject_practice_ids = [practice_subject[0]
                                                     for practice_subject in practice_subjects]

                    practices = practices.filter(
                        Practice.id.in_(practice_subject_practice_ids))

            pagination = practices.paginate(
                filters.get("page", 1),
                per_page=current_app.config["BODHICENTRAL_PRACTICES_PER_PAGE"],
                error_out=False
            )

            practices = pagination.items

            result = jsonify({
                "practices": [practice.to_json() for practice in practices],
                "total_count": pagination.total,
                "has_next": pagination.has_next
            })

        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}),
            ErrorCodes.HTTP_STATUS_BAD_REQUEST

        return result

    @staticmethod
    def get_single_practice(practice_id):
        try:
            practice = Practice.query.get(practice_id)

            if practice is None:
                raise PracticeNotFoundError

            result = jsonify(practice.to_json())

        except PracticeNotFoundError as e:
            result = jsonify({"error": e.error}
                             ), ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @classmethod
    def add_practice(cls, request):
        try:
            data = cls.__validate_data(request.json)
            subjects = data["subjects"]

            del data["subjects"]

            new_practice = Practice(data)
            new_practice.author = g.current_user

            params = [new_practice]

            for subject_id in subjects:
                params.append(PracticeSubject(
                    practice=new_practice, subject_id=subject_id))

            db.session.add_all(params)
            db.session.commit()

            result = jsonify(new_practice.to_json()
                             ), ErrorCodes.HTTP_STATUS_CREATED

        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}),
            ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except PostNotFoundError as e:
            result = jsonify({"error": e.error}),
            ErrorCodes.HTTP_STATUS_NOT_FOUND
        except SubjectNotFoundError as e:
            result = jsonify({"error": e.error}),
            ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @classmethod
    def edit_practice(cls, request, practice_id):
        try:
            practice = Practice.query.get(practice_id)

            if practice is None:
                raise PracticeNotFoundError

            data = cls.__validate_data(request.json)

            new_subjects = data["subjects"]

            current_subjects = [practice_subject.subject_id for practice_subject in PracticeSubject.query.filter_by(
                practice_id=practice.id)]

            subjects_to_add = [PracticeSubject(practice_id=practice_id,
                                               subject_id=subject_id)
                               for subject_id in new_subjects if subject_id not in current_subjects]

            subjects_to_delete = [
                subject_id for subject_id in current_subjects if subject_id not in new_subjects]

            del data["subjects"]

            practice.update_from_json(data)

            params = subjects_to_add + [practice]

            db.session.add_all(params)

            for subject_id in subjects_to_delete:
                PracticeSubject.query.filter(PracticeSubject.practice_id == practice_id,
                                             PracticeSubject.subject_id == subject_id).delete()

            db.session.commit()

            result = jsonify({"error": ErrorCodes.SUCCESS}
                             ), ErrorCodes.HTTP_STATUS_SUCCESS

        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}),
            ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except PostNotFoundError as e:
            result = jsonify({"error": e.error}),
            ErrorCodes.HTTP_STATUS_NOT_FOUND
        except SubjectNotFoundError as e:
            result = jsonify({"error": e.error}),
            ErrorCodes.HTTP_STATUS_NOT_FOUND
        except PracticeNotFoundError as e:
            result = jsonify({"error": e.error}),
            ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @staticmethod
    def delete_practice(practice_id):
        try:
            practice = Practice.query.get(practice_id)

            if practice is None:
                raise PracticeNotFoundError

            db.session.delete(practice)
            db.session.commit()

            result = jsonify({"error": ErrorCodes.SUCCESS}
                             ), ErrorCodes.HTTP_STATUS_SUCCESS

        except PracticeNotFoundError as e:
            result = jsonify({"error": e.error}),
            ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @staticmethod
    def __validate_data(data):
        data = PracticeSchema.validate(data)

        subjects = data["subjects"]

        data["post_id"] = data.get("post_id")

        post = None if data["post_id"] is None else Post.query.get(
            data["post_id"])

        if data["post_id"] is not None and post is None:
            raise PostNotFoundError

        for subject_id in subjects:
            if db.session.query(Subject.id).filter_by(id=subject_id).scalar() is None:
                raise SubjectNotFoundError

        return data
