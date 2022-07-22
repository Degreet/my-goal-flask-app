from flask import Blueprint, jsonify, make_response, render_template, request
from config import JWT_SECRET
from app import User, db
import jwt
import ast

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route('/dashboard')
def dashboard_page():
    return render_template("dashboard.html")


@dashboard_bp.route('/my_goal', methods=["GET"])
def get_my_goal():
    # получаем токен авторизации
    token = request.headers['authorization'].split(' ')[1]

    # если его нет, выдаем ошибку
    if not token or not len(token):
        return make_response(
            jsonify({ "ok": False, "error": "Unauthorized" }),
            401
        )

    # получаем информацию об авторизации через токен
    decoded = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=["HS256"])

    # ищем пользователя с таким айди
    user = User.query.get(decoded['id'])

    # отправляем ошибку если пользователь не найден
    if not user:
        return make_response(
            jsonify({ "ok": False, "error": "Unauthorized" }),
            401
        )

    if not user.goal or not user.goal_count:
        return jsonify({ "ok": True, "has": False })

    return jsonify({
        "ok": True,
        "has": True,
        "goal": user.goal,
        "goal_count": user.goal_count,
        "goal_done": user.goal_done
    })


@dashboard_bp.route('/create_my_goal', methods=["POST"])
def create_my_goal():
    # получаем токен авторизации
    token = request.headers['authorization'].split(' ')[1]

    # если его нет, выдаем ошибку
    if not token or not len(token):
        return make_response(
            jsonify({ "ok": False, "error": "Unauthorized" }),
            401
        )

    # получаем данные
    data = ast.literal_eval(request.data.decode('utf-8'))
    goal = data['goal']
    goal_count = data['goal_count']

    # проверяем данные
    if not goal or not len(goal) or not goal_count or not str(goal_count).isnumeric():
        return make_response(
            jsonify({ "ok": False, "error": "Incorrect data" }),
            400
        )

    # конвертируем в число (на всякий случай)
    goal_count = int(goal_count)

    # получаем информацию об авторизации через токен
    decoded = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=["HS256"])

    # ищем пользователя с таким айди
    user = User.query.get(decoded['id'])

    # отправляем ошибку если пользователь не найден
    if not user:
        return make_response(
            jsonify({ "ok": False, "error": "Unauthorized" }),
            401
        )

    # обновляем пользователя
    user.goal = goal
    user.goal_count = goal_count

    try:
        db.session.commit()
    except:
        return make_response(
            jsonify({ "ok": False, "error": "Server error" }),
            500
        )

    # отправляем сообщение об успехе
    return jsonify({ "ok": True })


@dashboard_bp.route('/up_my_goal', methods=["GET", "DELETE"])
def up_my_goal():
    # получаем токен авторизации
    token = request.headers['authorization'].split(' ')[1]

    # если его нет, выдаем ошибку
    if not token or not len(token):
        return make_response(
            jsonify({ "ok": False, "error": "Unauthorized" }),
            401
        )

    # получаем информацию об авторизации через токен
    decoded = jwt.decode(token.encode('utf-8'), JWT_SECRET, algorithms=["HS256"])

    # ищем пользователя с таким айди
    user = User.query.get(decoded['id'])

    # отправляем ошибку если пользователь не найден
    if not user:
        return make_response(
            jsonify({ "ok": False, "error": "Unauthorized" }),
            401
        )

    # проверяем, есть ли у пользователя цель
    if not user.goal or not user.goal_count:
        return make_response(
            jsonify({ "ok": False, "error": "Hasn't goal" }),
            400
        )

    # обновляем пользователя
    if request.method == "DELETE":
        user.goal_done = 0
    else: 
        user.goal_done += 1

    try:
        db.session.commit()
    except:
        return make_response(
            jsonify({ "ok": False, "error": "Server error" }),
            500
        )

    # отправляем сообщение об успехе
    return jsonify({ "ok": True })
