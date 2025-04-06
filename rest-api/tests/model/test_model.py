import unittest
from unittest.mock import MagicMock

from model_api.config.config import load_config
from model_api.model.model import SentimentModel


class TestSentimentModel(unittest.TestCase):
    def test_load_model(self):
        model_path = load_config('Test').MODEL_PATH
        preprocessor = MagicMock()
        model = SentimentModel(model_path, preprocessor)
        self.assertIsNotNone(model.get_model(), 'Error! Expected model to be not None')


if __name__ == '__main__':
    unittest.main()
