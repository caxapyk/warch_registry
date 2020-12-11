import os
import sys

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(basedir)

if os.environ.get('FLASK_ENV') != "development":
    activate_this = "%s/warch_registry/venv/bin/activate_this.py" % basedir
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

from warch_registry import create_app
application = create_app()
