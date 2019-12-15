from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify

from app import app
from flask import request
from models.user import User
from models.assignment import Assignment
from models.task import Task


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.find_by_email(data['email'])
    if user and check_password_hash(user.password, data["password"]):
        return jsonify({"login": True})
    return jsonify({"login": False})


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email_check = User.find_by_email(data['email'])
    if email_check:
        return jsonify({"signup": False})

    phone_number_check = User.find_by_phone_number(data['phone_number'])
    if phone_number_check:
        return jsonify({"signup": False})

    user = User(**data)
    user.password = generate_password_hash(data['password'], method="sha256")

    user.save()
    return jsonify({"signup": True})


@app.route("/user/<string:_id>/assignments", methods=["GET"])
def assignment_list(_id):
    # data = request.get_json()
    pass


@app.route("/user/<string:user_id>/assignments/<string:assignment_id>", methods=["GET", "POST"])
def assignment(user_id, assignment_id):
    # data = request.get_json()
    pass
