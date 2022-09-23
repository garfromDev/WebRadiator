from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NoneOf


class LoginForm(FlaskForm):
    username = StringField("Nom", validators=[DataRequired(), NoneOf(['toto', 'admin'])])
    password = PasswordField("Mor de passe", validators=[DataRequired(), Length(min=5)])
    remember_me = BooleanField("Se souvenir de moi")
    submit = SubmitField("S'identifier")

