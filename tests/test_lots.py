"""Story #5: As a driver, I want to see each lot's capacity and status.

Acceptance criteria:
  AC1 A lot under 75% occupied shows "open".
  AC2 A lot at 75% or more, but not full, shows "filling".
  AC3 A lot at or over capacity shows "full".
  AC4 The lots page lists every lot with spaces available.
"""
from app.services.lot_service import status_for


def test_ac1_open():
    assert status_for(capacity=100, occupied=74) == "open"


def test_ac2_filling_at_threshold():
    assert status_for(capacity=100, occupied=75) == "filling"
    assert status_for(capacity=100, occupied=99) == "filling"


def test_ac3_full():
    assert status_for(capacity=100, occupied=100) == "full"
    assert status_for(capacity=100, occupied=105) == "full"


def test_ac4_lots_page_lists_lots(client):
    resp = client.get("/lots/")
    assert resp.status_code == 200
    assert b"Lot 1 - Memorial Student Center" in resp.data
    assert b"180 of 220" in resp.data
