from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging
from flask_apscheduler import APScheduler
import signal
from Radiator.HeatMode import test

app = Flask(__name__)

def handle_sigterm(signum, frame):
    app.logger.info("SIGTERM reçu, nettoyage en cours...")
    # Ajoutez ici le code de nettoyage nécessaire
    # Par exemple, fermer des connexions de base de données, sauvegarder l'état, etc.
    if not test:
        import RPi.GPIO as GPIO
        GPIO.cleanup()  # release les ports GPIO utilisés par l'app
    app.logger.info("Nettoyage terminé, arrêt de l'application.")
    os._exit(0)


logger = logging.getLogger('werkzeug')  # grabs underlying WSGI logger
handler = logging.FileHandler('Radiator.log')  # creates handler for the log file
logger.addHandler(handler)
bootstrap = Bootstrap(app)
app.config.from_object(Config)  # TODO utiliser vraiment config
# Enregistrer le gestionnaire de signal pour SIGTERM et SIGINT, qui seront émis par systemctl
signal.signal(signal.SIGINT, handle_sigterm)
signal.signal(signal.SIGTERM, handle_sigterm)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # pour le suivi des migrations de la base

app.logger.debug("test" + os.environ.get("RADIATOR_TEST_ENVIRONMENT", ""))
app.logger.info("starting radiator")
appscheduler = APScheduler()
app.config['SCHEDULER_API_ENABLED'] = True
appscheduler.init_app(app)
appscheduler.start()
app.logger.info("scheduler started")

with app.app_context():
    from . import scheduler
    from . import routes
app.logger.debug("routes and scheduler loaded")
