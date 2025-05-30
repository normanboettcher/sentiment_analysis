import os

from flask import Flask
from flask_cors import CORS

from model_api.config.config import load_config
from model_api.routes.review_prediction import predict_bp


def create_app(config_name=None):
    app = Flask(__name__)
    app.logger.info(f"starting application with config profile: {config_name}")
    app.config.from_object(load_config(config_name))

    origins = os.getenv('ALLOWED_ORIGINS', '').split(',')
    print(f'start up application with allowed origins: {[origin for origin in origins]}')

    CORS(app, origins=origins)
    app.register_blueprint(predict_bp)
    return app
