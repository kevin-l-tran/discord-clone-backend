import requests

from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import create_access_token

from .models import User

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
    return jsonify({"access_token": access_token}), 200


@auth.route("/signup", methods=["POST"])
def signup():
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not username:
        return jsonify({"err": "Missing username"}), 400
    if not email:
        return jsonify({"err": "Missing email"}), 400
    if not password:
        return jsonify({"err": "Missing password"}), 400

    if User.objects(name__iexact=username).first():
        return jsonify({"err": "Username taken"}), 409
    if User.objects(email__iexact=email).first():
        return jsonify({"err": "Email taken"}), 409

    # email validate api
    api_url = "https://api.api-ninjas.com/v1/validateemail?email={}".format(email)
    try:
        response = requests.get(
            api_url, headers={"X-Api-Key": current_app.config["NINJA_API_KEY"]}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"err": "Update failed", "details": str(e)}), 502
    else:
        if not response.json()["is_valid"]:
            return jsonify({"err": "Invalid email"}), 422
        if response.json()["is_disposable"]:
            return jsonify({"err": "Disposable email"}), 422

    # profanity check api
    api_url = "https://api.api-ninjas.com/v1/profanityfilter?text={}".format(username)
    try:
        response = requests.get(
            api_url, headers={"X-Api-Key": current_app.config["NINJA_API_KEY"]}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"err": "Update failed", "details": str(e)}), 502
    else:
        if response.json()["has_profanity"]:
            return jsonify({"err": "Username has profanity"}), 422

    if len(username) < 4:
        return jsonify({"err": "Username too short"}), 422
    if len(password) < 8:
        return jsonify({"err": "Password too short"}), 422

    user = User()
    user.name = username
    user.email = email
    user.set_password(password)
    user.save(force_insert=True)

    access_token = create_access_token(identity=username)
    return (
        jsonify({"access_token": access_token}),
        201,
        #jsonify({"Location": url_for("get_user", username=username, _external=True)}),
    )


@auth.route("/check/<string:email>", methods=["GET"])
def check_email(email):
    api_url = "https://api.api-ninjas.com/v1/validateemail?email={}".format(email)
    try:
        response = requests.get(
            api_url, headers={"X-Api-Key": current_app.config["NINJA_API_KEY"]}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"err": "Update failed", "details": str(e)}), 502
    else:
        if not response.json()["is_valid"]:
            return jsonify({"err": "Invalid email"}), 422
        if response.json()["is_disposable"]:
            return jsonify({"err": "Disposable email"}), 422

        return jsonify({"msg": "Good email"}), 200
