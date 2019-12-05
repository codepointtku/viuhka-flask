from flask_wtf                          import FlaskForm
from wtforms.validators                 import length, DataRequired
from wtforms                            import StringField, PasswordField


class RegisterForm(FlaskForm):
    username        = StringField('Username', [DataRequired(), length(max=32)])
    email           = StringField('Email', [DataRequired(), length(max=100)])
    password        = PasswordField('Password', [DataRequired(), length(max=100)])