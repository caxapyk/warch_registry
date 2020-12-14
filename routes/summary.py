from flask import render_template

from warch_registry.app import auth, bp_summary


@bp_summary.route("/")
@auth.login_required
def index():
    return render_template('summary/index.html')
