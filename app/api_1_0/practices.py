from . import api
from flask import request
from ..modules.BCPractice import BCPractice
from .authentication import auth


@api.route("/practice", methods=["GET"])
@auth.login_required
def get_practices():
    return BCPractice.get_practices(request)


@api.route("/practice/<int:practice_id>", methods=["GET"])
@auth.login_required
def get_single_practice(practice_id):
    return BCPractice.get_single_practice(practice_id)


@api.route("/practice", methods=["POST"])
@auth.login_required
def add_practice():
    return BCPractice.add_practice(request)


@api.route("/practice/<int:practice_id>", methods=["PUT"])
@auth.login_required
def edit_practice(practice_id):
    return BCPractice.edit_practice(request, practice_id)


@api.route("/practice/<int:practice_id>", methods=["DELETE"])
@auth.login_required
def delete_practice(practice_id):
    return BCPractice.delete_practice(practice_id)
