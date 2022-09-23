from app import app
from flask import render_template, redirect, flash
import random

from app.forms import LoginForm
from InsideCondition import InsideCondition

class Radiator:
    @property
    def temperature(self):
        return random.randint(15,25)

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
def main_page():
    radiator = InsideCondition.shared()
    return render_template('index.html', title='Radiator', radiator=radiator, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login_post():
    # TODO login
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for("index"))
    return render_template('login.html', title='Sign In', form=form)