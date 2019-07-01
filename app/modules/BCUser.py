from ..db_models import User
from flask import jsonify
from .. import db
# from .schemas.post_schema import PostSchema, PostQSPSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
# from ..exceptions import PostNotFoundError, SubjectNotFoundError


class BCUser:
    @staticmethod
    def add_user(request):
        print(request.json)
        try:
            result = jsonify({"hi": "hi"})
        except SchemaError:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
                ErrorCodes.HTTP_STATUS_BAD_REQUEST

        return result
