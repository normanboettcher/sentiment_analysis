import os

from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from model_api.config.config import load_config
from model_api.routes.metrics import metrics_bp
from model_api.routes.review_prediction import predict_bp


def create_app(config_name=None):
    app = Flask(__name__)
    app.logger.info(f"starting application with config profile: {config_name}")
    app.config.from_object(load_config(config_name))

    origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    print(
        f"start up application with allowed origins: {[origin for origin in origins]}"
    )

    CORS(app, origins=origins)
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api_bp.register_blueprint(predict_bp)
    api_bp.register_blueprint(metrics_bp)
    app.register_blueprint(api_bp)
    return app
