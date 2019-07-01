from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized, forbidden
from ..db_models.User import User
from . import api
from ..modules.BCUser import BCUser

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if password == "":
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized("Invalid Credentials")


@auth.login_required
def before_request():
    if not g.current_user.confirmed:
        return forbidden("Unconfirmed account")


@api.route("/token")
@auth.login_required
def get_token():
    if g.token_used:
        return unauthorized("Invalid credentials")
    return jsonify({"token": g.current_user.generate_auth_token(expiration=3600), "expiration": 3600})


@api.route("/verify-token")
@auth.login_required
def verify_token():
    return jsonify({"error": 200})


@api.route("/sign-up", methods=["POST"])
def add_user():
    return BCUser.add_user(request)


@api.route("/confirm/<token>")
def confirm(token):
    return BCUser.confirm_user(token)
