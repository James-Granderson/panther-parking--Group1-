"""Story #1: As a driver, I want to create an account and log in.

Acceptance criteria (one test each):
  AC1 A new email with an 8+ character password creates an account.
  AC2 A password under 8 characters is rejected with a message.
  AC3 The same email cannot register twice.
  AC4 The right password logs the user in; the wrong one does not.
"""
from app.repositories import user_repository


def test_ac1_register_creates_account(client, app):
    client.post("/auth/register", data={"email": "new@pvamu.edu", "password": "longenough"})
    with app.app_context():
        assert user_repository.find_by_email("new@pvamu.edu") is not None


def test_ac2_short_password_rejected(client, app):
    resp = client.post("/auth/register", data={"email": "a@pvamu.edu", "password": "short"},
                       follow_redirects=True)
    assert b"at least 8 characters" in resp.data
    with app.app_context():
        assert user_repository.find_by_email("a@pvamu.edu") is None


def test_ac3_duplicate_email_rejected(client):
    data = {"email": "dup@pvamu.edu", "password": "panthers123"}
    client.post("/auth/register", data=data)
    resp = client.post("/auth/register", data=data, follow_redirects=True)
    assert b"already exists" in resp.data


def test_ac4_login_right_and_wrong_password(client, register_and_login):
    resp = register_and_login()
    assert resp.status_code == 302  # redirected to the lots page
    client.get("/auth/logout")
    resp = client.post("/auth/login", data={"email": "student@pvamu.edu", "password": "wrongpass"},
                       follow_redirects=True)
    assert b"Incorrect email or password" in resp.data
