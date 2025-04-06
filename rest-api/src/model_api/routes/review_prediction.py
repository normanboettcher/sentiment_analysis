from flask import request, jsonify, current_app
from flask import Blueprint

from model_api.services.sentiment_service import get_sentiment

predict_bp = Blueprint('predict', __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    review = data.get('review', '')

    if not review:
        return jsonify({"error": "No review provided"}), 400

    config = current_app.config
    result = get_sentiment(review, config)
    return jsonify(result)
