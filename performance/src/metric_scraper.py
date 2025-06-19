import subprocess
import json
from enum import Enum


class MetricLabels(Enum):
    AVG_REQUEST_TIME_TOTAL = "avg_request_time_total"


class MetricScraper:
    def __init__(self, api_endpoint="api/v1", api_host="http://localhost:9090"):
        self._api_endpoint = api_endpoint
        self._api_host = api_host

    def _get_metric_as_json(self, query: str) -> dict:
        try:
            result = subprocess.run(
                ["curl",
                 f"{self._api_host}/{self._api_endpoint}/query?query={query}"],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f'Error scraping metric with query {query}', e)
            raise

    def get_avg_request_time_total(self):
        json_data = self._get_metric_as_json("sum(request_predict_seconds_sum)/sum(request_predict_seconds_count)")
        print(f'request time: {json_data["data"]["result"][0]["value"][1]} seconds')

    def collect_and_reset(self, n_reviews: str, reset=True, write_output=True):
        # collect the metrics into a dictionary where each entry is the amount of reviews containing another dictionary
        # where the key is the metric name
        if n_reviews is None:
            raise ValueError("Please provide a quantity of reviews")
        try:
            reviews_amount = int(n_reviews)
        except (ValueError, TypeError) as error:
            raise ValueError(f'Could not parse {n_reviews} to a number: {error}')
