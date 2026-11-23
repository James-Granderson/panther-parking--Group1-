"""Business rules for permits. No Flask request objects and no SQL here."""
from ..repositories import lot_repository, permit_repository, vehicle_repository


class PermitError(Exception):
    """Raised with a user-facing message when a permit rule is broken."""


def apply(user_id, vehicle_id_raw, zone):
    zone = (zone or "").strip()
    try:
        vehicle_id = int(vehicle_id_raw)
    except (TypeError, ValueError):
        raise PermitError("Choose one of your vehicles.")

    vehicle = vehicle_repository.find_by_id(vehicle_id)
    if vehicle is None or vehicle["user_id"] != user_id:
        raise PermitError("That vehicle isn't registered to you.")
    if zone not in lot_repository.list_zones():
        raise PermitError("Choose a zone that exists.")
    if permit_repository.find_active(vehicle_id, zone):
        raise PermitError(
            "You already have a permit application for this vehicle and zone."
        )
    return permit_repository.create(vehicle_id, zone)


def dashboard_for(user_id):
    return {
        "permits": permit_repository.list_for_user(user_id),
        "vehicles": vehicle_repository.list_for_user(user_id),
        "zones": lot_repository.list_zones(),
    }


def pending_permits():
    return permit_repository.list_pending()


def decide(permit_id, decision):
    if decision not in ("approved", "rejected"):
        raise PermitError("Choose approve or reject.")
    permit = permit_repository.find_by_id(permit_id)
    if permit is None:
        raise PermitError("That permit does not exist.")
    if permit["status"] != "pending":
        raise PermitError("That permit has already been decided.")
    permit_repository.set_status(permit_id, decision)
