import json
import unittest
from subprocess import CompletedProcess
from unittest.mock import patch

from performance.utils.metric_scraper import MetricScraper


class TestMetricScraper(unittest.TestCase):

    @patch("performance.utils.metric_scraper.subprocess.run")
    def test_get_avg_request_time_total_called_prometheus(self, subprocess_mock):
        scraper = MetricScraper()
        args = [
            "curl",
            "http://localhost:9090/api/v1/query?query=sum(request_predict_seconds_sum)/sum(request_predict_seconds_count)"
        ]
        response = {
            "data": {
                "result": [{"value": [1, 3]}]
            }
        }
        subprocess_mock.return_value = CompletedProcess(args=args, stdout=json.dumps(response), returncode=0)
        result = scraper.get_avg_request_time_total()

        self.assertIsNotNone(result, 'Expected result to be not None')
        self.assertEqual(result, 3, "Expected total avg response time to be 3")
        subprocess_mock.assert_called_once_with(args,
                                                capture_output=True,
                                                text=True,
                                                check=True)
