import unittest
from unittest.mock import MagicMock
from model_api.routes.review_prediction import create_app


class ReviewPredictionTestCase(unittest.TestCase):
    def setUp(self):
        self.model_mock = MagicMock()

    def test_predict_success(self):
        self.model_mock.predict.return_value = {'sentiment': 'positive'}
        app = create_app(self.model_mock).test_client()
        response = app.post('/predict', json={'review': 'What a great movie!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sentiment'], 'positive')
        self.assertIn('sentiment', response.json)
        self.model_mock.predict.assert_called_once_with('What a great movie!')

    def test_predict_missing_review(self):
        # a model should not be neccessary since the method returns an error before
        # model interaction
        app = create_app(None).test_client()
        response = app.post('/predict', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main()
