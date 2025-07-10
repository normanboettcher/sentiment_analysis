import unittest
from logging import getLogger
from unittest.mock import patch

from .test_app import create_test_app

logger = getLogger('IntegrationTests')


class IntegrationTests(unittest.TestCase):
    def test_success_prediction(self):
        app = create_test_app().test_client()
        response = app.post('/predict', json={'review': 'What a really great movie!'})
        print(f'prediction for review [What a really great movie!] is: [{response.json}]')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sentiment', response.json)

    @patch('model_api.services.sentiment_service.get_lookup_table')
    def test_failure_lookup_table_reading(self, get_lookup_table_mock):
        app = create_test_app().test_client()
        get_lookup_table_mock.side_effect = RuntimeError('Error reading lookup table for testcase')
        response = app.post('/predict', json={'review': 'What a really great movie!'})
        print(f'response for failure reading lookup table: [{response.json}]')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main()
