from flask import Flask
from config import Config
import os
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
# at this point, ENV doesn't contain ENV variables declared in Pycharm settings

app = Flask(__name__)
app.config.from_object(Config)
#print("secret :", app.config['RADIATOR_TEST_ENVIRONMENT'])
print("secret :", app.config['SECRET_KEY'])
os.environ["RADIATOR_TEST_ENVIRONMENT"] = "TRUE"
sys.path.append('/Users/alistef/Documents/Programmation/Rasberry/Radiator/')
from  main import start_radiator
print("staring radiator")
os.chdir('/Users/alistef/Documents/Programmation/Rasberry/Radiator/')
start_radiator()

from app import routes