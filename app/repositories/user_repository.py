from ..db import get_db


def find_by_email(email):
    row = get_db().execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
    return dict(row) if row else None


def find_by_id(user_id):
    row = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def create(email, password_hash, role="driver"):
    db = get_db()
    cur = db.execute(
        "INSERT INTO user (email, password_hash, role) VALUES (?, ?, ?)",
        (email, password_hash, role),
    )
    db.commit()
    return cur.lastrowid
