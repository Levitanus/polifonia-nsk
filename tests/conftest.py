import pytest

from random import randint

from polyphony_app.app import create_app, db, migrate
from polyphony_app.users.models import User
from polyphony_app.users.forms import LoginForm


@pytest.fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite://',
            'WTF_CSRF_ENABLED': False,
        }
    )
    # migrate.

    context = app.app_context()
    context.push()
    db.create_all()
    # db.session.configure
    yield app
    db.session.remove()
    db.drop_all()
    context.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, app, client):
        self._client = client
        if db.session.query(User).filter('username' == 'test').first():
            return
        u = User(username='test', password='test', email='test@test.test')
        db.session.add(u)
        db.session.commit()

    def login(self, username='test', password='test', follow_redirects=False):
        form = LoginForm(None, username=username, password=password)
        return self._client.post(
            '/users/auth', data=form.data, follow_redirects=follow_redirects
        )

    def logout(self):
        return self._client.get('/users/logout')

    def add_user(self, username: str, password: str) -> User:
        u = User(
            username=username,
            password=password,
            email=f'test{randint(0,10000)}@test.test'
        )
        db.session.add(u)
        db.session.commit()
        return u

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, type, value, traceback):
        self.logout()


@pytest.fixture
def auth(app, client):
    return AuthActions(app, client)
