import unittest
from unittest.mock import patch

from performance.utils.metric_scraper import MetricScraper


class TestMetricScraper(unittest.TestCase):

    @patch("performance.utils.metric_scraper.PrometheusClient.get_scalar_value")
    def test_get_avg_request_time_total_called_prometheus(self, prometheus_client_mock):
        # given
        scraper = MetricScraper()
        query = "sum(request_predict_seconds_sum)/sum(request_predict_seconds_count)"
        prometheus_client_mock.return_value = 3
        # when
        result = scraper.get_avg_request_time_predict_total()

        # then
        self.assertIsNotNone(result, 'Expected result to be not None')
        self.assertEqual(result, 3, "Expected total avg response time to be 3")
        prometheus_client_mock.assert_called_once_with(query)
