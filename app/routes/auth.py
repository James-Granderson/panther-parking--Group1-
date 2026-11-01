import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from ..repositories import user_repository
from ..services import auth_service
from ..services.auth_service import AuthError

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = user_repository.find_by_id(user_id) if user_id else None


def login_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        try:
            auth_service.register(request.form.get("email"), request.form.get("password"))
            flash("Account created. Please log in.")
            return redirect(url_for("auth.login"))
        except AuthError as e:
            flash(str(e))
    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        try:
            user = auth_service.authenticate(request.form.get("email"), request.form.get("password"))
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("lots.index"))
        except AuthError as e:
            flash(str(e))
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
