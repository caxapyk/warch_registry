from flask import render_template

from warch_registry import auth, bp_main


@bp_main.route("/")
@auth.login_required
def index():
    return render_template('index/index.html')
