from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import logging
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
# at this point, ENV doesn't contain ENV variables declared in Pycharm settings

app = Flask(__name__)
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) #
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'  # so flask know how to log users
app.config.from_object(Config)  # TODO utiliser vraiment config
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # pour le suivi des migrations de la base

app.logger.info("test" + os.environ.get("RADIATOR_TEST_ENVIRONMENT", ""))
from Radiator.main import start_radiator
app.logger.info("starting radiator")
with app.app_context():
    start_radiator(app, avoid_flash=True)

from app import routes, models