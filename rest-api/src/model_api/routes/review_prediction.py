from flask import request, jsonify, current_app
from flask import Blueprint
from prometheus_client import Summary, Counter
from model_api.services.sentiment_service import get_sentiment

predict_bp = Blueprint("predict", __name__)

REQUEST_TIME = Summary('request_predict_seconds', 'Time spent processing request')
REQUEST_SUCCESS = Counter('request_predict_success', 'Count of successfull requests of /predict')
REQUEST_FAILURE = Counter('request_predict_failure', 'Count of failured requests of /predict')


@REQUEST_TIME.time()
@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    review = data.get("review", "")
    if not review:
        return jsonify({"error": "No review provided"}), 400

    config = current_app.config
    result = get_sentiment(review, config)
    if result.get("error") is not None:
        return jsonify(result), 400
    REQUEST_SUCCESS.inc()
    return jsonify(result)
