from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
# at this point, ENV doesn't contain ENV variables declared in Pycharm settings

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'  # so flask know how to log users
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # pour le suivi des migrations de la base

print("test :", app.config['RADIATOR_TEST_ENVIRONMENT'])
print("secret :", app.config['SECRET_KEY'])
os.environ["RADIATOR_TEST_ENVIRONMENT"] = str(app.config['RADIATOR_TEST_ENVIRONMENT'])
print("test", os.environ.get("RADIATOR_TEST_ENVIRONMENT"))
from Radiator.main import start_radiator
print("starting radiator")
start_radiator(app, avoid_flash=True)

from app import routes, models