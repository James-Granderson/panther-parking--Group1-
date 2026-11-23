import os
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.db import init_db
from app.repositories import user_repository


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


@pytest.fixture
def login_as_admin(app, client):
    def _do(email="admin@pvamu.edu", password="adminpass123"):
        with app.app_context():
            user_repository.create(email, generate_password_hash(password), role="admin")
        return client.post("/auth/login", data={"email": email, "password": password})
    return _do
