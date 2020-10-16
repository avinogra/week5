import flask
from flask import Flask, render_template,  request, abort, session, redirect
from sqlalchemy.sql.expression import func
from datetime import datetime
from forms import RegistrationForm, OrderForm, LoginForm
from app import app, db
from models import db, Order, Meal, Category, User
from hashlib import md5
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)

admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view((ModelView(Order, db.session)))


@app.route('/')
def home():

    categories = db.session.query(Category).order_by(Category.id.desc()).all()

    # грузим рандомные блюда для категорий
    cat_meals = []
    for cat in categories:
        meal = db.session.query(Meal).filter(Meal.category_id == cat.id).\
                order_by(func.random()).limit(3)
        cat_meals.append([cat.id, cat.title, meal])

    return render_template('main.html', cat_meals=cat_meals)


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() and (request.method == "POST"):
        user = User.query.filter_by(mail=form.mail.data).first()
        if user:
            form.mail.errors.append("Пользователь с таким Email уже существует")
            return render_template("register.html", form=form)
        new_user = User(
            mail=form.mail.data,
            password=md5(form.password.data.encode()).hexdigest()
        )
        db.session.add(new_user)
        db.session.commit()
        user = db.session.query(User).filter(User.mail == form.mail.data).first()
        session['user_id'] = user.id
        return redirect('/account/')
    return render_template('register.html', form=form)


@app.route('/addtocart/<int:meal>/')
def addtochart(meal):
    price = db.session.query(Meal).get(meal).price
    session['cart_id'] = session.get('cart_id', [])
    session['cart_price'] = session.get('cart_price', [])
    session['cart_id'].append(str(meal))
    session['cart_price'].append(price)
    return redirect('/cart/')


# удаляем товар из корзины
@app.route('/delfromcart/<meal>/')
def delfromcart(meal):
    session.modified = True
    # проверка есть ли блюдо в списке выбранных
    if meal in session['cart_id']:
        idx = session['cart_id'].index(meal)
        session['cart_id'].pop(idx)
        session['cart_price'].pop(idx)
        session['deleted'] = True
        return redirect('/cart/')
    else:
        return abort(404, 'Блюдо не может быть удалено')


@app.route('/cart/', methods=["GET", "POST"])
def cart():
    deleted = session['deleted']
    session['deleted'] = False
    form = OrderForm()
    if form.validate_on_submit():
        order = Order()
        user = db.session.query(User).get(session['user_id'])
        order.user_id = user.id
        order.amount = sum(list(map(int, session.get('cart_price'))))
        order.name = flask.request.form.get('name')
        order.phone = flask.request.form.get('phone')
        order.address = flask.request.form.get('address')
        order.mail = flask.request.form.get('mail')
        order.date = datetime.now()
        order.status = 'Принят'
        meals = list(map(int, session.get('cart_id')))
        for meal in meals:
            meal = db.session.query(Meal).get(meal)
            order.meals.append(meal)
        db.session.add(order)
        db.session.commit()
        session['cart_id'] = []
        session['cart_price'] = []
        return redirect('/ordered/')

    else:
        meals = []
        for meal in session.get('cart_id'):
            meal = db.session.query(Meal).get(meal)
            meals.append(meal)
            # Проверяем прошел ли пользователь аутентификацию
        if session.get('user_id'):
            user = db.session.query(User).get(session['user_id'])
            form.mail.data = user.mail
    return render_template('cart.html', meals=meals, form=form, deleted=deleted)


# вход пользователя в систему
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if (request.method == "POST"):
        user = db.session.query(User).filter(User.mail == form.email.data).first()
        if user and user.password == md5(form.password.data.encode()).hexdigest():
            session['user_id'] = user.id
            return redirect('/account/')

        errors = list(form.email.errors)
        errors.append("Неверный email или пароль.")
        form.email.errors = tuple(errors)
    return render_template('login.html', form=form)


@app.route('/ordered/')
def ordered():
    return render_template('ordered.html')


@app.route('/account/')
def account():
    if session.get('user_id'):
        user = db.session.query(User).get(session['user_id'])
        return render_template('account.html', orders=user.orders)
    return abort(404, 'Вы не авторизированы. Необходимо пройти регистрацию и \
         войти в личный кабинет.')


@app.route('/logout/')
def logout():
    session['user_id'] = None
    session['cart_id'] = []
    session['cart_price'] = []
    return redirect('/login/')
