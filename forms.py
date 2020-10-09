from flask_wtf import FlaskForm
import re
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, InputRequired, Required
# from wtforms.validators import DataRequired, email_validator,Length, ValidationError
from wtforms import StringField, IntegerField, SubmitField, PasswordField
# from wtforms.fields.html5 import TelField
from flask_wtf.csrf import CSRFProtect

import re
def password_check(form, field):
    msg = "Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры"
    rexes = ('[A-Z]', '[a-z]', '[0-9]')
    if not( all(re.search(r, field.data) for r in rexes) ):
        raise ValidationError(msg)




class RegistrationForm(FlaskForm):
    mail = StringField('Электропочта', [DataRequired(),
    Length(min=5, max=100, message="Введите от 5 до 30 символов")])
    password = PasswordField("Пароль:", \
        validators=[DataRequired(),
                # Пароль не менее 8 символов
                Length(min=8, message="Пароль должен быть не менее 8 символов"),
                password_check
            ]
        )

class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [DataRequired(),
        Length(min=2, max=30, message="Введите от 2 до 30 символов")])
    address = StringField('Адрес', [DataRequired(),
        Length(min=10, max=200, message="Введите от 10 до 200 символов")])
    mail = StringField('Электропочта', [DataRequired(),
        Length(min=5, max=100, message="Введите от 5 до 30 символов")])
    phone = TelField('Телефон', [DataRequired(),
        Length(min=10, max=20, message="Введите от 10 до 20 символов")])

class LoginForm(FlaskForm):
    email = StringField("Электропочта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])