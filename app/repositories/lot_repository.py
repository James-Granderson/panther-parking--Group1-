from ..db import get_db


def list_all():
    rows = get_db().execute("SELECT * FROM lot ORDER BY name").fetchall()
    return [dict(r) for r in rows]


def find_by_id(lot_id):
    row = get_db().execute("SELECT * FROM lot WHERE id = ?", (lot_id,)).fetchone()
    return dict(row) if row else None


def find_by_name(name):
    row = get_db().execute("SELECT * FROM lot WHERE name = ?", (name,)).fetchone()
    return dict(row) if row else None


def create(name, zone, capacity):
    db = get_db()
    cur = db.execute(
        "INSERT INTO lot (name, zone, capacity) VALUES (?, ?, ?)",
        (name, zone, capacity),
    )
    db.commit()
    return cur.lastrowid


def update(lot_id, name, zone, capacity):
    db = get_db()
    db.execute(
        "UPDATE lot SET name = ?, zone = ?, capacity = ? WHERE id = ?",
        (name, zone, capacity, lot_id),
    )
    db.commit()


def list_zones():
    rows = get_db().execute("SELECT DISTINCT zone FROM lot ORDER BY zone").fetchall()
    return [row["zone"] for row in rows]
