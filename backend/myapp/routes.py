from flask import Blueprint, request, jsonify
from .models import User, Task
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main_routes = Blueprint("main_routes", __name__)

# ---------------- TEST ----------------
@main_routes.route("/test")
def test():
    return {"message": "Backend working"}


# ---------------- REGISTER ----------------
@main_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = generate_password_hash(data.get("password"))

    if User.query.filter_by(username=username).first():
        return {"message": "User already exists"}, 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}


# ---------------- LOGIN ----------------
@main_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not check_password_hash(user.password, data.get("password")):
        return {"message": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "message": "Login successful",
        "access_token": access_token
    }


# ---------------- PROFILE ----------------
@main_routes.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    return {
        "id": user.id,
        "username": user.username
    }


# ---------------- CREATE TASK ----------------
@main_routes.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    task = Task(
        title=data.get("title"),
        user_id=int(user_id)
    )

    db.session.add(task)
    db.session.commit()

    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    }


# ---------------- GET TASKS ----------------
@main_routes.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=int(user_id)).all()

    result = []
    for t in tasks:
        result.append({
            "id": t.id,
            "title": t.title,
            "completed": t.completed
        })

    return result


# ---------------- UPDATE TASK ----------------
@main_routes.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    task = Task.query.filter_by(id=task_id, user_id=int(user_id)).first()

    if not task:
        return {"message": "Task not found"}, 404

    task.title = data.get("title", task.title)
    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return {"message": "Task updated"}


# ---------------- DELETE TASK ----------------
@main_routes.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=int(user_id)).first()

    if not task:
        return {"message": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return {"message": "Task deleted"}