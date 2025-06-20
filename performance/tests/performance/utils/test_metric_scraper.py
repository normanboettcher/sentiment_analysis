import unittest
from subprocess import CompletedProcess
from unittest.mock import patch
from performance.src.performance.utils.metric_scraper import MetricScraper


class TestMetricScraper(unittest.TestCase):

    @patch("metric_scraper.subprocess")
    def test_get_avg_request_time_total_called_prometheus(self, subprocess_mock):
        scraper = MetricScraper()
        subprocess_mock.return_value = CompletedProcess(stdout="{\"test\": \"returned\"}", returncode=0)
        result = scraper.get_avg_request_time_total()

        self.assertIsNotNone(result, 'Expected result to be not None')
        subprocess_mock.assert_called_once_with(["curl",
                                                 "http://localhost:9090/api/v1/query?query=sum(request_predict_seconds_sum)/sum(request_predict_seconds_count)"],
                                                capture_output=True,
                                                text=True,
                                                check=True)
