from flask import Flask
from .api.endpoints.login import login_blueprint
from .api.endpoints.register import register_blueprint
from .api.endpoints.logout import logout_blueprint
from .dependencies import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings.DevelopmentConfig')

    # Registering blueprints
    app.register_blueprint(login_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(logout_blueprint)

    init_db(app.config)

    return app
