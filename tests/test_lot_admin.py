"""Story #6: As a Parking Office admin, I want to create and edit lots
(name, zone, capacity), so that the system matches campus.

Acceptance criteria:
  AC1 An admin who submits a name, zone and capacity creates a lot that appears
      on the lots page.
  AC2 An admin who edits a lot's name, zone or capacity sees the new values.
  AC3 Invalid capacities, including values below current occupancy, are rejected.
  AC4 A lot name already used by another lot is rejected.
  AC5 A driver who opens the create or edit page is redirected, with no lot changes.
"""
import pytest

from app.db import get_db

NEW_LOT = {"name": "Lot 99 - Test Lot", "zone": "Student", "capacity": "50"}


def lot_count(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM lot").fetchone()[0]


def test_ac1_admin_creates_lot(client, login_as_admin):
    login_as_admin()
    client.post("/lots/new", data=NEW_LOT)
    resp = client.get("/lots/")
    assert b"Lot 99 - Test Lot" in resp.data
    assert b"50 of 50" in resp.data


def test_ac2_admin_edits_lot(client, login_as_admin):
    login_as_admin()
    client.post(
        "/lots/1/edit",
        data={"name": "Lot 1 - Renamed", "zone": "Faculty/Staff", "capacity": "300"},
    )
    resp = client.get("/lots/")
    assert b"Lot 1 - Renamed" in resp.data
    assert b"260 of 300" in resp.data


@pytest.mark.parametrize("capacity", ["0", "-5", "abc", "10.5", ""])
def test_ac3_bad_capacity_rejected_on_create(client, app, login_as_admin, capacity):
    login_as_admin()
    resp = client.post(
        "/lots/new", data={**NEW_LOT, "capacity": capacity}, follow_redirects=True
    )
    assert b"Capacity must be a whole number above 0." in resp.data
    assert lot_count(app) == 3


def test_ac3_capacity_below_occupied_rejected_on_edit(client, login_as_admin):
    login_as_admin()
    resp = client.post(
        "/lots/2/edit",
        data={
            "name": "Lot 7 - Harrington Science",
            "zone": "Student",
            "capacity": "100",
        },
        follow_redirects=True,
    )
    assert b"lower than the 120 spaces occupied" in resp.data
    assert b"30 of 150" in client.get("/lots/").data


def test_ac4_duplicate_name_rejected(client, app, login_as_admin):
    login_as_admin()
    resp = client.post(
        "/lots/new",
        data={**NEW_LOT, "name": "Lot 1 - Memorial Student Center"},
        follow_redirects=True,
    )
    assert b"A lot with that name already exists." in resp.data
    assert lot_count(app) == 3
    resp = client.post(
        "/lots/2/edit",
        data={
            "name": "Lot 1 - Memorial Student Center",
            "zone": "Student",
            "capacity": "150",
        },
        follow_redirects=True,
    )
    assert b"A lot with that name already exists." in resp.data


def test_ac5_driver_cannot_create_or_edit(client, app, register_and_login):
    register_and_login()
    responses = [
        client.get("/lots/new"),
        client.post("/lots/new", data=NEW_LOT),
        client.get("/lots/1/edit"),
        client.post(
            "/lots/1/edit",
            data={"name": "Hacked", "zone": "Student", "capacity": "10"},
        ),
    ]
    assert all(response.status_code == 302 for response in responses)
    assert lot_count(app) == 3
    assert b"Hacked" not in client.get("/lots/").data
