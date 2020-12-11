import os
from flask import Flask, Blueprint, render_template
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
auth = HTTPBasicAuth()

bp_main = Blueprint('main', 'warch_registry.routes.main')
bp_inventory = Blueprint('inventory', 'warch_registry.routes.inventory')
bp_registry = Blueprint('registry', 'warch_registry.routes.registry')

def create_app(config='warch_registry.config.Default'):
    app = Flask(__name__)
    app.config.from_object(config)
    if os.environ.get('WARCH_REGISTRY_SETTINGS'):
        app.config.from_envvar('WARCH_REGISTRY_SETTINGS')

    db.init_app(app)

    with app.app_context():
        from warch_registry.routes import main, inventory, registry
        import warch_registry.context_processors
        import warch_registry.error
        import warch_registry.user
        
        app.register_blueprint(bp_main, url_prefix='/')
        app.register_blueprint(bp_inventory, url_prefix='/registry')
        app.register_blueprint(bp_registry, url_prefix='/registries')

        return app
