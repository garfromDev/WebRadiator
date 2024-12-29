import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "nimportequoi"
    RADIATOR_TEST_ENVIRONMENT = os.environ.get('RADIATOR_TEST_ENVIRONMENT', "False")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(base_dir, "app.db"))
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATION = False  # evite d'envoyer un signal à chaque modif de la base
