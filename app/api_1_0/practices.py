from . import api
from flask import request
from ..modules.BCPractice import BCPractice


@api.route("/practice", methods=["GET"])
def get_practices():
    return BCPractice.get_practices(request)


@api.route("/practice/<int:practice_id>", methods=["GET"])
def get_single_practice(practice_id):
    return BCPractice.get_single_practice(practice_id)


@api.route("/practice", methods=["POST"])
def add_practice():
    return BCPractice.add_practice(request)


@api.route("/practice/<int:practice_id>", methods=["PUT"])
def edit_practice(practice_id):
    return BCPractice.edit_practice(request, practice_id)


@api.route("/practice/<int:practice_id>", methods=["DELETE"])
def delete_practice(practice_id):
    return BCPractice.delete_practice(practice_id)
