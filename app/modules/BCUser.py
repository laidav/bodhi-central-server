from ..db_models import User
from flask import jsonify
from .. import db
from .schemas.auth_schema import AddUserSchema
from .ErrorCodes import ErrorCodes
from schema import SchemaError
from ..exceptions import UsernameAlreadyExistsError, EmailAlreadyExistsError, ConfirmPasswordError
from ..email import send_email


class BCUser:
    @classmethod
    def add_user(cls, request):
        try:
            data = cls.__validate_data(request.json)
            new_user = User(data)

            db.session.add(new_user)
            db.session.commit()
            token = new_user.generate_confirmation_token()
            send_email(new_user.email, "Confirm your account",
                       "auth/email/confirm", user=new_user, token=token)

            result = jsonify(new_user.to_json())
        except SchemaError as e:
            result = jsonify({"error": ErrorCodes.SCHEMA_VALIDATION}), \
                ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except UsernameAlreadyExistsError as e:
            result = jsonify({"error": e.error}
                             ), ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except EmailAlreadyExistsError as e:
            result = jsonify({"error": e.error}
                             ), ErrorCodes.HTTP_STATUS_BAD_REQUEST
        except ConfirmPasswordError as e:
            result = jsonify({"error": e.error}
                             ), ErrorCodes.HTTP_STATUS_BAD_REQUEST

        return result

    @classmethod
    def __validate_data(cls, data):
        data = AddUserSchema.validate(data)

        if data["password"] != data["password2"]:
            raise ConfirmPasswordError

        cls.__check_existing_username(data["username"])
        cls.__check_existing_email(data["email"])

        return data

    @staticmethod
    def __check_existing_username(username):
        if User.query.filter_by(username=username).first():
            raise UsernameAlreadyExistsError

    @staticmethod
    def __check_existing_email(email):
        if User.query.filter_by(email=email).first():
            raise EmailAlreadyExistsError
