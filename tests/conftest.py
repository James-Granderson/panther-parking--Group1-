import os
import tempfile

import pytest

from app import create_app
from app.db import init_db


@pytest.fixture
def app():
    fd, path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": path, "SECRET_KEY": "test"})
    with app.app_context():
        init_db()
    yield app
    os.close(fd)
    os.unlink(path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def register_and_login(client):
    def _do(email="student@pvamu.edu", password="panthers123"):
        client.post("/auth/register", data={"email": email, "password": password})
        return client.post("/auth/login", data={"email": email, "password": password})
    return _do
