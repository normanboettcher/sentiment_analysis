from flask import Flask
from model_api.routes.review_prediction import predict_bp
from model_api.config import load_config


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(load_config(config_name))
    app.register_blueprint(predict_bp)
    return app
