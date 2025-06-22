from enum import Enum

from performance.utils.prometheus_client import PrometheusClient


class MetricLabels(Enum):
    AVG_REQUEST_TIME_TOTAL = "avg_request_time_total"


class MetricScraper:
    def __init__(self, prometheus_client=None):
        self._prometheus_client = prometheus_client or PrometheusClient()

    def get_avg_request_time_predict_total(self) -> float:
        query = "sum(request_predict_seconds_sum)/sum(request_predict_seconds_count)"
        value = self._prometheus_client.get_scalar_value(query)
        print(f"avg_request_time_predict_total: {value}")
        return value

    def collect_and_reset(self, n_reviews: str, reset=True, write_output=True):
        # collect the metrics into a dictionary where each entry is the amount of reviews containing another dictionary
        # where the key is the metric name
        if n_reviews is None:
            raise ValueError("Please provide a quantity of reviews")
        try:
            reviews_amount = int(n_reviews)
        except (ValueError, TypeError) as error:
            raise ValueError(f'Could not parse {n_reviews} to a number: {error}')
