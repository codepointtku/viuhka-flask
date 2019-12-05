from flask_wtf                              import FlaskForm
from wtforms.validators                     import length, DataRequired
from wtforms                                import StringField, PasswordField


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), length(max=32)])
    password = PasswordField('Password', [DataRequired(), length(max=100)])