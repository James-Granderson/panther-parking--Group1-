from flask import Blueprint, render_template

from ..services import lot_service

bp = Blueprint("lots", __name__, url_prefix="/lots")


@bp.route("/")
def index():
    return render_template("lots.html", lots=lot_service.lots_with_status())
