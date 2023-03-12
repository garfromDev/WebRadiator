from app import app
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import random
from .models import User

from app.forms import LoginForm, RadiatorForm
from Radiator.InsideCondition import InsideCondition
from Radiator.main import decider


class Radiator:
    @property
    def temperature(self):
        return random.randint(15, 25)

    @property
    def connected(self):
        return bool(random.choice([True, False]))


posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
]


@app.route('/')
@login_required
def main_page():
    radiator = InsideCondition.shared()
    form = RadiatorForm()
    if form.validate_on_submit():
        if form.eco.data:
            print("=== eco mode")
            decider._heater._setEcoMode()
    return render_template('index.html', title='Radiator', radiator=radiator, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # domain is a full domain, not an inside domain  of my site -> forbidden
            next_page = url_for('main_page')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/mode/<heating_mode>')
@login_required
def mode(heating_mode):
    print("=== choosen heating mode : %s" % heating_mode)
    return redirect(url_for('main_page'))
