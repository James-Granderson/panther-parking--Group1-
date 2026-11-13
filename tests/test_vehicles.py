"""Story #2: As a driver, I want to register a vehicle (plate, make, model, color),
so that it can be linked to a permit.

Acceptance criteria (one test each):
  AC1 A logged-in driver who submits plate, make, model and color sees the vehicle in their list.
  AC2 A plate longer than 8 characters, or with anything other than letters and digits,
      is rejected with a message and nothing is saved.
  AC3 A plate already registered to another driver is rejected with
      "This plate is already registered."
  AC4 A blank make, model or color is rejected with a message and nothing is saved.
  AC5 A visitor who is not logged in is redirected to the login page.
"""
import pytest

from app.db import get_db

GOOD = {"plate": "ABC123", "make": "Toyota", "model": "Corolla", "color": "Blue"}


def vehicle_count(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM vehicle").fetchone()[0]


def test_ac1_registered_vehicle_appears_in_list(client, register_and_login):
    register_and_login()
    client.post("/vehicles/", data=GOOD)
    resp = client.get("/vehicles/")
    assert b"ABC123" in resp.data
    assert b"Toyota" in resp.data


@pytest.mark.parametrize("plate", ["ABCDEFGHI", "AB-123", "AB 123", ""])
def test_ac2_bad_plate_rejected(client, app, register_and_login, plate):
    register_and_login()
    resp = client.post("/vehicles/", data={**GOOD, "plate": plate}, follow_redirects=True)
    assert b"Plate must be" in resp.data
    assert vehicle_count(app) == 0


def test_ac3_duplicate_plate_rejected(client, app, register_and_login):
    register_and_login("a@pvamu.edu")
    client.post("/vehicles/", data=GOOD)
    client.get("/auth/logout")
    register_and_login("b@pvamu.edu")
    resp = client.post("/vehicles/", data=GOOD, follow_redirects=True)
    assert b"This plate is already registered." in resp.data
    assert vehicle_count(app) == 1


@pytest.mark.parametrize("field", ["make", "model", "color"])
def test_ac4_blank_field_rejected(client, app, register_and_login, field):
    register_and_login()
    resp = client.post("/vehicles/", data={**GOOD, field: "  "}, follow_redirects=True)
    assert b"Make, model and color are required." in resp.data
    assert vehicle_count(app) == 0


def test_ac5_visitor_redirected_to_login(client):
    resp = client.get("/vehicles/")
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]
