from . import api
from flask import request
from ..modules.BLPractice import BLPractice


@api.route("/practice", methods=["GET"])
def get_practices():
    return BLPractice.get_practices(request)


@api.route("/practice", methods=["POST"])
def add_practice():
    return BLPractice.add_practice(request)


@api.route("/practice/<int:practice_id>", methods=["PUT"])
def edit_practice(practice_id):
    return BLPractice.edit_practice(request, practice_id)
