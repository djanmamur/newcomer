from flask import Blueprint, jsonify

from functions import retrieve_repos

blueprint = Blueprint("routes", __name__)


@blueprint.route("/repositories", methods=["GET"])
def get_repositories():
    return jsonify(retrieve_repos())
