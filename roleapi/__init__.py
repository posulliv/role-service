import os

from flask import Flask
from roleapi.config import config

def create_app(app_environment=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if app_environment is None:
        app = Flask(__name__)
        app.config.from_object(config[os.getenv('FLASK_ENV', 'dev')])
    else:
        app = Flask(__name__)
        app.config.from_object(config[app_environment])

    from roleapi import role
    
    app.register_blueprint(role.bp)

    from roleapi import extensions
    extensions.trino.init_app(app)

    return app