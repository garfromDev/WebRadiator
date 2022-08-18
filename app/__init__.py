from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
print("secret :", app.config['SECRET_KEY'])

from app import routes