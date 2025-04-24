import os

from flask import Flask
from model_api.routes.review_prediction import predict_bp


class TestConfig:
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "Sentiment-M7.keras",
    )
    LOOKUP_TABLE_PATH = os.path.join(
        os.path.dirname(__file__),
        "lookup_table.json",
    )
    VOCAB_SIZE = "10000"
    NUM_OOV_BUCKETS = "1000"
    FRONTEND_HOST = 'localhost'
    FRONTEND_PORT = '5000'


def create_test_app():
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    app.register_blueprint(predict_bp)
    return app
