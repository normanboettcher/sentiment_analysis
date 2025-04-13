from logging import getLogger

from flask import Flask

from model_api.config.config import load_config
from model_api.routes.review_prediction import predict_bp

logger = getLogger("app.py")


def create_app(config_name=None):
    app = Flask(__name__)
    logger.info(f"starting application with config profile: {config_name}")
    app.config.from_object(load_config(config_name))
    app.register_blueprint(predict_bp)
    return app
