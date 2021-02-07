import os
_basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('POLYPHONY_SECRET') or 'you_will_newer_guess'
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'POLYPHONY_DB_URL'
) or 'sqlite:///' + os.path.join(_basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
