from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # создаем приложение
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id пользователя
    login = db.Column(db.String(20), nullable=False) # логин
    password = db.Column(db.String(64), nullable=False) # пароль
    goal = db.Column(db.String(64), nullable=True) # цель
    goal_count = db.Column(db.Integer, nullable=True) # кол-во повторений на день
    goal_done = db.Column(db.Integer, default=0) # выполнено
    date = db.Column(db.DateTime, default=datetime.utcnow) # дата регистрации

    def __repr__(self):
        return "<User %r>" % self.id


if __name__ == "__main__":
    from routes import setup_routes
    setup_routes(app) # регистрируем роуты
    app.run(debug=True, port=3000) # запускаем сервер production
