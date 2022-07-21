import json
from flask import Blueprint, make_response, request, render_template, jsonify
from config import JWT_SECRET
from app import User, db

import bcrypt
import jwt
import ast


login_bp = Blueprint("login", __name__)


@login_bp.route('/login', methods=["GET", "POST"])
def log_in_page():
    if request.method == "GET": # если пользователь перешел по адресу
        return render_template("login.html") # рендерим страницу логина

    data = ast.literal_eval(request.data.decode('utf-8'))
    login = data["login"] # получаем логин
    password = data["password"] # получаем пароль

    if not login or len(login) < 3: # если некорректный логин
        return { "ok": False, "error": "Incorrect login" }
    elif not password or len(password) < 8: # если некорректный пароль
        return { "ok": False, "error": "Incorrect password" }

    # ищем пользователя с таким логином
    candidate = User.query.filter_by(login=login).first()

    # энкодим пароль
    password = password.encode('utf-8')

    # если пользователь есть, не регистрируем, но даем токен
    if candidate:
        # проверяем пароль
        compare = bcrypt.checkpw(password, candidate.password.encode('utf-8'))

        if compare:
            token = jwt.encode({ "id": candidate.id }, JWT_SECRET)
            return jsonify({ "ok": True, "token": token })
        else:
            return make_response(
                { "ok": False, "error": "Incorrect login data" },
                400
            ) 
    
    # хешируем пароль
    password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    # создаем пользователя
    user = User(login=login, password=password)

    # сохраняем в базу данных
    try:
        db.session.add(user)
        db.session.commit()
    except:
        # если не удалось, отправляем ошибку
        return make_response(
            { "ok": False, "error": "Server error" },
            500
        )

    # создаем токен для сохранения авторизации
    token = jwt.encode({ "id": user.id }, JWT_SECRET, algorithm="HS256")
    
    # отправляем сообщение об успехе
    return jsonify({ "ok": True, "token": token })
