"""Business rules for vehicles. No Flask request objects and no SQL here."""
import re

from ..repositories import vehicle_repository

PLATE_PATTERN = re.compile(r"[A-Z0-9]{1,8}")


class VehicleError(Exception):
    """Raised with a user-facing message when a rule is broken."""


def register(user_id, plate, make, model, color):
    plate = (plate or "").strip().upper()
    make = (make or "").strip()
    model = (model or "").strip()
    color = (color or "").strip()
    if not PLATE_PATTERN.fullmatch(plate):
        raise VehicleError("Plate must be 1-8 letters and digits.")
    if not (make and model and color):
        raise VehicleError("Make, model and color are required.")
    if vehicle_repository.find_by_plate(plate):
        raise VehicleError("This plate is already registered.")
    return vehicle_repository.create(user_id, plate, make, model, color)


def vehicles_for(user_id):
    return vehicle_repository.list_for_user(user_id)
