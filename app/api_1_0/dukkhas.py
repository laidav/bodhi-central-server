from . import api
from flask import jsonify


@api.route("/dukkhas")
def get_dukkhas():
    return jsonify({"dukkhas": "dukkhas!"})
