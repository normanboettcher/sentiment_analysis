from flask import Flask
from flask_cors import CORS

from model_api.config.config import load_config
from model_api.routes.review_prediction import predict_bp


def create_app(config_name=None):
    app = Flask(__name__)
    app.logger.info(f"starting application with config profile: {config_name}")
    app.config.from_object(load_config(config_name))

    host_url, target_port = app.config.get("FRONTEND_HOST_URL"), app.config.get(
        "FRONTEND_PORT"
    )

    CORS(app, origins=[f"http://{host_url}:{target_port}"])
    app.register_blueprint(predict_bp)
    return app
