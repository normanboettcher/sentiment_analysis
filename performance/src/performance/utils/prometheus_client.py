# performance/utils/prometheus_client.py
import requests


class PrometheusClient:
    def __init__(self, base_url="http://localhost:9090"):
        self.base_url = base_url.rstrip("/")

    def query(self, promql: str) -> dict:
        url = f"{self.base_url}/api/v1/query"
        try:
            response = requests.get(url, params={"query": promql})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to fetch Prometheus data for query '{promql}':", e)
            raise

    def get_scalar_value(self, promql: str) -> float:
        json_data = self.query(promql)
        try:
            return float(json_data["data"]["result"][0]["value"][1])
        except (KeyError, IndexError, ValueError) as e:
            print("Unexpected or malformed Prometheus response:", json_data)
            raise
