from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..services import lot_service
from ..services.lot_service import LotError
from .auth import admin_required

bp = Blueprint("lots", __name__, url_prefix="/lots")


@bp.route("/")
def index():
    return render_template("lots.html", lots=lot_service.lots_with_status())


@bp.route("/new", methods=("GET", "POST"))
@admin_required
def new():
    if request.method == "POST":
        try:
            lot_service.create_lot(
                request.form.get("name"),
                request.form.get("zone"),
                request.form.get("capacity"),
            )
            flash("Lot created.")
            return redirect(url_for("lots.index"))
        except LotError as error:
            flash(str(error))
    return render_template("lot_form.html", lot=None)


@bp.route("/<int:lot_id>/edit", methods=("GET", "POST"))
@admin_required
def edit(lot_id):
    try:
        lot = lot_service.get_lot(lot_id)
    except LotError as error:
        flash(str(error))
        return redirect(url_for("lots.index"))
    if request.method == "POST":
        try:
            lot_service.update_lot(
                lot_id,
                request.form.get("name"),
                request.form.get("zone"),
                request.form.get("capacity"),
            )
            flash("Lot updated.")
            return redirect(url_for("lots.index"))
        except LotError as error:
            flash(str(error))
    return render_template("lot_form.html", lot=lot)
