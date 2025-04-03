import unittest
import json
from model_api.review_prediction import app
from unittest.mock import patch


class ReviewPredictionTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.SentimentModel')
    def test_predict_success(self, MockSentimentModel):
        model_mock = MockSentimentModel.return_value
        model_mock.predict.return_value = {'sentiment': 'positive'}
        response = self.client.post('/predict', json={'review', 'What a great movie!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sentiment'], 'positive')
        self.assertIn('sentiment', response.json)
        model_mock.predict.assert_called_once_with('What a great movie!')

    def test_predict_missing_review(self):
        response = self.client.post('/predict', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main()
