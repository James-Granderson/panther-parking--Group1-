from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..services import permit_service
from ..services.permit_service import PermitError
from .auth import admin_required, login_required

bp = Blueprint("permits", __name__, url_prefix="/permits")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        try:
            permit_service.apply(
                g.user["id"],
                request.form.get("vehicle_id"),
                request.form.get("zone"),
            )
            flash("Permit application submitted.")
            return redirect(url_for("permits.index"))
        except PermitError as error:
            flash(str(error))
    return render_template(
        "permits.html", **permit_service.dashboard_for(g.user["id"])
    )


@bp.route("/review")
@admin_required
def review():
    return render_template(
        "review.html", permits=permit_service.pending_permits()
    )


def _decide(permit_id, decision):
    try:
        permit_service.decide(permit_id, decision)
        flash(f"Permit {decision}.")
    except PermitError as error:
        flash(str(error))
    return redirect(url_for("permits.review"))


@bp.route("/<int:permit_id>/approve", methods=("POST",))
@admin_required
def approve(permit_id):
    return _decide(permit_id, "approved")


@bp.route("/<int:permit_id>/reject", methods=("POST",))
@admin_required
def reject(permit_id):
    return _decide(permit_id, "rejected")
