import flask
from flask import Flask
from flask_migrate import Migrate


from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from models import db, Order, Meal, Category, User

# Настраиваем соединение
db.init_app(app)
# Создаем объект поддержки миграций
migrate = Migrate(app, db)


from forms import RegistrationForm, OrderForm, LoginForm


# Имортируем представление
from views import *

if __name__ == '__main__':
    app.run()
