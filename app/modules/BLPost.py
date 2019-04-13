from ..db_models import Post, Subject, PostSubject
from flask import g, jsonify
from .. import db
from .schemas.post_schema import PostSchema, PostQSPSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import PostNotFoundError, SubjectNotFoundError
from .BLTree import BLTree


class BLPost:
    @staticmethod
    def get_posts(request):
        try:
            filters = PostQSPSchema.validate(request.args.to_dict(flat=False))

            subjects = []

            if "subject_id" in filters:
                for subject_id in filters["subject_id"]:
                    subject = Subject.query.get(subject_id)

                    if subject is not None:
                        subjects = subjects + BLTree.get_descendants(subject) \
                            if subject_id not in subjects else subjects

            subjects = set(subjects)

            post_subjects = PostSubject.query

            if len(subjects):
                post_subjects = post_subjects.filter(PostSubject.subject_id.in_(subjects))

            post_subjects = post_subjects.distinct(PostSubject.post_id).group_by(PostSubject.post_id).all()

            result = jsonify({"posts": [post_subject.post.to_json() for post_subject in post_subjects]}), ErrorCodes.\
                HTTP_STATUS_SUCCESS
        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
                     ErrorCodes.HTTP_STATUS_BAD_REQUEST

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
        except SubjectNotFoundError:
            result = jsonify({"error": ErrorCodes.SUBJECT_NOT_FOUND}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result

    @classmethod
    def edit_post(cls, request, post_id):
        try:
            post = Post.query.get(post_id)

            if post is None:
                raise PostNotFoundError

            data = cls.__validate_data(request.json)

            new_subjects = data["subjects"]

            current_subjects = [post_subject.subject_id for post_subject in PostSubject.query.filter_by(
                post_id=post.id)]

            subjects_to_add = [PostSubject(post_id=post_id, subject_id=subject_id)
                               for subject_id in new_subjects if subject_id not in current_subjects]

            subjects_to_delete = [subject_id for subject_id in current_subjects if subject_id not in new_subjects]

            del data["subjects"]

            post.update_from_json(data)

            params = subjects_to_add + [post]

            db.session.add_all(params)

            for subject_id in subjects_to_delete:
                PostSubject.query.filter(PostSubject.post_id == post_id,
                                         PostSubject.subject_id == subject_id).delete()

            db.session.commit()

            return jsonify({"error": ErrorCodes.SUCCESS}), ErrorCodes.HTTP_STATUS_SUCCESS

        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
                     ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except PostNotFoundError as e:
            result = jsonify({"error": e.error}), ErrorCodes.HTTP_STATUS_NOT_FOUND
        except SubjectNotFoundError as e:
            result = jsonify({"error": e.error}), \
                     ErrorCodes.HTTP_STATUS_NOT_FOUND

        return result
    
    @staticmethod
    def delete_post(post_id):
        try:
            post = Post.query.get(post_id)

            if post is None:
                raise PostNotFoundError

            db.session.delete(post)
            db.session.commit()

            result = jsonify({"error": ErrorCodes.SUCCESS}), ErrorCodes.HTTP_STATUS_SUCCESS

        except PostNotFoundError as e:
            result = jsonify({"error": e.error}), \
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
