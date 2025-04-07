import unittest
from unittest.mock import MagicMock, patch

from sentiment_model.text_preprocessing import ReviewPreprocessor
from ..test_resources.test_config import TestConfig

from model_api.model.model import SentimentModel


class TestSentimentModel(unittest.TestCase):
    def test_load_model(self):
        model_path = TestConfig.MODEL_PATH
        preprocessor = MagicMock()
        model = SentimentModel(model_path, preprocessor)
        self.assertIsNotNone(model.get_model(), 'Error! Expected model to be not None')

    @patch('tensorflow.keras.models.load_model')
    def test_load_model_not_found(self, tf_keras_load_model_mock):
        tf_keras_load_model_mock.side_effect = FileNotFoundError('Not found here')
        with self.assertRaises(Exception):
            model = SentimentModel('wrong/path', MagicMock())

    def test_predict_empty_review(self):
        review = ''
        model = SentimentModel(TestConfig.MODEL_PATH, MagicMock())
        result = model.predict(review)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Review text is empty.')

    def test_predict_success(self):
        import tensorflow as tf
        review = 'it is not empty'
        mock_preprocessor = MagicMock(spec=ReviewPreprocessor)
        mock_preprocessor.prepare_data_set.return_value = tf.constant([[0, 1, 2, 3]])
        model = SentimentModel(TestConfig.MODEL_PATH, mock_preprocessor)
        result = model.predict(review)
        self.assertIn('sentiment', result)

    def test_predict_value_error(self):
        review = 'regular review'
        mock_preprocessor = MagicMock(spec=ReviewPreprocessor)
        mock_preprocessor.prepare_data_set.side_effect = ValueError('Oh No! Value Error here!')
        model = SentimentModel(TestConfig.MODEL_PATH, mock_preprocessor)
        result = model.predict(review)

        self.assertIn('error', result)
        self.assertEqual(result['error'], 'An unexpected error occurred. Please try again later.')


if __name__ == '__main__':
    unittest.main()
