from flask import Flask

from api import routes
from settings import ProductionConfig


def create_app(config_object=ProductionConfig):
    application = Flask(__name__)
    application.config.from_object(config_object)

    register_blueprints(application)
    return application


def register_blueprints(application):
    application.register_blueprint(routes.blueprint)
