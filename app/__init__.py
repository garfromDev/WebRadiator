from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging
from flask_apscheduler import APScheduler


app = Flask(__name__)
logger = logging.getLogger('werkzeug')  # grabs underlying WSGI logger
handler = logging.FileHandler('test.log')  # creates handler for the log file
logger.addHandler(handler)
bootstrap = Bootstrap(app)
app.config.from_object(Config)  # TODO utiliser vraiment config
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # pour le suivi des migrations de la base

logger.info("test" + os.environ.get("RADIATOR_TEST_ENVIRONMENT", ""))
logger.info("starting radiator")
appscheduler = APScheduler()
app.config['SCHEDULER_API_ENABLED'] = True
appscheduler.init_app(app)
appscheduler.start()
app.logger.info("scheduler started")

with app.app_context():
    from . import scheduler
    from . import routes
app.logger.info("routes and scheduler loaded")
