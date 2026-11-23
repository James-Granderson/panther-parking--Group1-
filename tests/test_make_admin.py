"""Supporting task for story #4: how an account becomes an admin.

The Parking Office runs: flask --app app make-admin EMAIL

Acceptance criteria:
  AC1 The command gives an existing account the admin role.
  AC2 An email with no account is reported as an error and nothing changes.
"""
from app.repositories import user_repository


def test_ac1_make_admin_promotes_existing_account(client, app):
    client.post("/auth/register", data={"email": "boss@pvamu.edu", "password": "panthers123"})
    result = app.test_cli_runner().invoke(args=["make-admin", "boss@pvamu.edu"])
    assert result.exit_code == 0
    with app.app_context():
        assert user_repository.find_by_email("boss@pvamu.edu")["role"] == "admin"


def test_ac2_make_admin_unknown_email_is_an_error(client, app):
    result = app.test_cli_runner().invoke(args=["make-admin", "nobody@pvamu.edu"])
    assert result.exit_code != 0
    assert "No account" in result.output
