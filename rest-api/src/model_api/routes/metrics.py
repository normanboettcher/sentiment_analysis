from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from model_api.routes.review_prediction import predict_bp


@predict_bp.route("/metrics", methods=["POST"])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
