from flask import Blueprint
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
