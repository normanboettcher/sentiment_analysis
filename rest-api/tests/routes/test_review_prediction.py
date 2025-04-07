import unittest
from unittest.mock import patch, ANY
from ..test_resources.test_config import create_test_app


class ReviewPredictionTestCase(unittest.TestCase):

    @patch('model_api.routes.review_prediction.get_sentiment')
    def test_predict_success(self, get_sentiment_mock):
        get_sentiment_mock.return_value = {'sentiment': 'positive'}
        app = create_test_app().test_client()
        response = app.post('/predict', json={'review': 'What a great movie!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sentiment'], 'positive')
        self.assertIn('sentiment', response.json)
        get_sentiment_mock.assert_called_once_with('What a great movie!', ANY)

    def test_predict_missing_review(self):
        # a model should not be neccessary since the method returns an error before
        # model interaction
        app = create_test_app().test_client()
        response = app.post('/predict', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main()
