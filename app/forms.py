from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NoneOf
from enum import Enum


class InteractionChoices(Enum):
    confort = "Confort"
    eco = "Eco"
    more_heat = "Plus chaud"
    less_heat = "Moins chaud"
    off = "Off"


class LoginForm(FlaskForm):
    username = StringField("Nom", validators=[DataRequired(), NoneOf(['toto', 'admin'])])
    password = PasswordField("Mor de passe", validators=[DataRequired(), Length(min=5)])
    remember_me = BooleanField("Se souvenir de moi")
    submit = SubmitField("S'identifier")


class RadiatorForm(FlaskForm):
    confort = SubmitField(InteractionChoices.confort.value, render_kw={"class": "button"})
    eco = SubmitField(InteractionChoices.eco.value)
    off = SubmitField(InteractionChoices.off.value)
    more_heat = SubmitField(InteractionChoices.more_heat.value)
    less_heat = SubmitField(InteractionChoices.less_heat.value)
