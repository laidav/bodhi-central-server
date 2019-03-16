from . import api
from ..database import Dukkha
from flask import g, jsonify


@api.route("/dukkhas")
def get_dukkhas():

    dukkhas = Dukkha.query.filter_by(author=g.current_user)

    return jsonify({
        "dukkhas": [dukkha.to_json() for dukkha in dukkhas]
    })
