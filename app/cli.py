"""Commands the Parking Office runs from the terminal."""
import click
from flask.cli import with_appcontext

from .services import auth_service
from .services.auth_service import AuthError


@click.command("make-admin")
@click.argument("email")
@with_appcontext
def make_admin_command(email):
    """Give an existing account the admin role."""
    try:
        auth_service.make_admin(email)
    except AuthError as error:
        raise click.ClickException(str(error))
    click.echo(f"{email} is now an admin.")
