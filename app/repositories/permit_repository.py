from ..db import get_db


def create(vehicle_id, zone):
    db = get_db()
    cur = db.execute(
        "INSERT INTO permit (vehicle_id, zone) VALUES (?, ?)", (vehicle_id, zone)
    )
    db.commit()
    return cur.lastrowid


def find_active(vehicle_id, zone):
    row = get_db().execute(
        "SELECT * FROM permit WHERE vehicle_id = ? AND zone = ? "
        "AND status IN ('pending', 'approved')",
        (vehicle_id, zone),
    ).fetchone()
    return dict(row) if row else None


def list_for_user(user_id):
    rows = get_db().execute(
        "SELECT permit.*, vehicle.plate FROM permit "
        "JOIN vehicle ON vehicle.id = permit.vehicle_id "
        "WHERE vehicle.user_id = ? ORDER BY permit.id",
        (user_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def find_by_id(permit_id):
    row = get_db().execute(
        "SELECT * FROM permit WHERE id = ?", (permit_id,)
    ).fetchone()
    return dict(row) if row else None


def list_pending():
    rows = get_db().execute(
        "SELECT permit.*, vehicle.plate, user.email FROM permit "
        "JOIN vehicle ON vehicle.id = permit.vehicle_id "
        "JOIN user ON user.id = vehicle.user_id "
        "WHERE permit.status = 'pending' ORDER BY permit.id"
    ).fetchall()
    return [dict(row) for row in rows]


def set_status(permit_id, status):
    db = get_db()
    db.execute("UPDATE permit SET status = ? WHERE id = ?", (status, permit_id))
    db.commit()
