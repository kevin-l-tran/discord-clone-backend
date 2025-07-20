from flask import Blueprint, request, jsonify
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned
from flask_jwt_extended import create_access_token

from models import User

auth = Blueprint("auth", __name__)


@auth.route("/signin", methods=["POST"])
def signin():
    username = request.json.get("name", None)
    password = request.json.get("password", None)

    if not username:
        return jsonify({"err": "Missing username"}), 400
    if not password:
        return jsonify({"err": "Missing password"}), 400

    user = User.objects.get(name__iexact=username)

    if not user:
        return jsonify({"err": "Bad username"}), 401
    if not user.check_password(password):
        return jsonify({"err": "Bad password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
