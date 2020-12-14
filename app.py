import os
from flask import Flask, Blueprint, render_template
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
auth = HTTPBasicAuth()

bp_main = Blueprint('main', 'warch_registry.routes.main')
bp_inventory = Blueprint('inventory', 'warch_registry.routes.inventory')
bp_inventory_type = Blueprint(
    'inventory_type', 'warch_registry.routes.inventory_type')
bp_registry = Blueprint('registry', 'warch_registry.routes.registry')

def create_app(config='warch_registry.config.Default'):
    app = Flask(__name__)
    app.config.from_object(config)

    # load configuration from settings.cfg
    basedir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir))
    cfg_file = "%s/warch_registry/settings.cfg" % basedir
    if os.path.exists(cfg_file):
        app.config.from_pyfile(cfg_file)

    db.init_app(app)

    with app.app_context():
        from warch_registry.routes import main, inventory, inventory_type, registry
        import warch_registry.context_processors
        import warch_registry.error
        import warch_registry.user
        
        app.register_blueprint(bp_main, url_prefix='/')
        app.register_blueprint(bp_inventory, url_prefix='/registry')
        app.register_blueprint(bp_inventory_type, url_prefix='/inventory-type')
        app.register_blueprint(bp_registry, url_prefix='/registries')

        return app
