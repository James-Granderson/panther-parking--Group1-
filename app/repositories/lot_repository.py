from ..db import get_db


def list_all():
    rows = get_db().execute("SELECT * FROM lot ORDER BY name").fetchall()
    return [dict(r) for r in rows]
