from . import api
from flask import jsonify


@api.route("/users")
def get_users():
    return jsonify({"users": "users!"})
