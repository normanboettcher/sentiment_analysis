from flask import request, jsonify, current_app
from flask import Blueprint
from prometheus_client import Summary, Counter, Histogram
from model_api.services.sentiment_service import get_sentiment

predict_bp = Blueprint("predict", __name__)

REQUEST_TIME_HISTOGRAM = Histogram(
    "request_predict_seconds_histogram",
    "Time spent processing request histogram specific",
)
REQUEST_TIME = Summary("request_predict_seconds", "Time spent processing the request")
REQUEST_SUCCESS = Counter(
    "request_predict_success", "Count of successfully requests of /predict"
)
REQUEST_FAILURE = Counter(
    "request_predict_failure", "Count of failure requests of /predict"
)
REVIEW_LENGTH = Summary("review_length", "Review lengths sent from users")


@predict_bp.route("/predict", methods=["POST"])
@REQUEST_TIME_HISTOGRAM.time()
@REQUEST_TIME.time()
def predict():
    data = request.get_json()
    review = data.get("review", "")
    if not review:
        REQUEST_FAILURE.inc()
        return jsonify({"error": "No review provided"}), 400

    REVIEW_LENGTH.observe(len(review))
    config = current_app.config
    result = get_sentiment(review, config)
    if result.get("error") is not None:
        REQUEST_FAILURE.inc()
        return jsonify(result), 400
    REQUEST_SUCCESS.inc()
    return jsonify(result)
