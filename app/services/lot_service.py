"""Business rules for parking lots."""
from ..repositories import lot_repository

FILLING_THRESHOLD = 0.75  # 75% occupied or more = "filling"


class LotError(Exception):
    """Raised with a user-facing message when a lot rule is broken."""


def _lot_fields(name, zone, capacity_raw):
    name = (name or "").strip()
    zone = (zone or "").strip()
    if not name or not zone:
        raise LotError("Lot name and zone are required.")
    try:
        capacity = int(capacity_raw)
    except (TypeError, ValueError):
        raise LotError("Capacity must be a whole number above 0.")
    if capacity <= 0:
        raise LotError("Capacity must be a whole number above 0.")
    return name, zone, capacity


def status_for(capacity, occupied):
    """Return 'open', 'filling' or 'full' for a lot.

    Story #5 acceptance criteria live in tests/test_lots.py.
    """
    if occupied >= capacity:
        return "full"
    if occupied / capacity >= FILLING_THRESHOLD:
        return "filling"
    return "open"


def lots_with_status():
    lots = lot_repository.list_all()
    for lot in lots:
        lot["status"] = status_for(lot["capacity"], lot["occupied"])
        lot["available"] = max(lot["capacity"] - lot["occupied"], 0)
    return lots


def get_lot(lot_id):
    lot = lot_repository.find_by_id(lot_id)
    if lot is None:
        raise LotError("That lot does not exist.")
    return lot


def create_lot(name, zone, capacity_raw):
    name, zone, capacity = _lot_fields(name, zone, capacity_raw)
    if lot_repository.find_by_name(name):
        raise LotError("A lot with that name already exists.")
    return lot_repository.create(name, zone, capacity)


def update_lot(lot_id, name, zone, capacity_raw):
    lot = get_lot(lot_id)
    name, zone, capacity = _lot_fields(name, zone, capacity_raw)
    existing = lot_repository.find_by_name(name)
    if existing and existing["id"] != lot_id:
        raise LotError("A lot with that name already exists.")
    if capacity < lot["occupied"]:
        raise LotError(
            f"Capacity cannot be lower than the {lot['occupied']} spaces occupied."
        )
    lot_repository.update(lot_id, name, zone, capacity)
