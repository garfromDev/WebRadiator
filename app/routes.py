from app import app
from flask import render_template
import random

from app.forms import LoginForm


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
    radiator = Radiator()
    return render_template('index.html', title='Radiator', radiator=radiator, posts=posts)

@app.route("/login", method=["GET", "POST"])
def login():
    form = LoginForm()

    return render_template("login.html", title="Login", form=form)
