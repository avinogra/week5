import flask
from flask import Flask
from flask_migrate import Migrate
from models import db, Order, Meal, Category, User
from forms import RegistrationForm, OrderForm, LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Настраиваем соединение
db.init_app(app)
# Создаем объект поддержки миграций
migrate = Migrate(app, db)

# Импортируем представление
from views import *

if __name__ == '__main__':
    app.run()
