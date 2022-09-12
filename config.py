import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "nimportequoi"
    #RADIATOR_TEST_ENVIRONMENT = os.environ.get('RADIATOR_TEST_ENVIRONMENT') or False