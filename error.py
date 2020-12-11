from flask import current_app,render_template
from sqlalchemy import exc
from werkzeug.exceptions import HTTPException, InternalServerError


@current_app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return e

    # wrapped unhandled error
    return render_template("500_generic.html", e=original), 500


@current_app.errorhandler(exc.SQLAlchemyError)
def handle_exception(e):
    # pass through IntegrityError
    if isinstance(e, exc.IntegrityError):
       return render_template("500_integrity.html", e=e), 500

    return render_template("500_generic.html", e=e), 502
