import importlib
import os
import unittest
from unittest.mock import patch

from model_api import config
from model_api.model import SentimentModel


class TestSentimentModel(unittest.TestCase):
    @patch.dict(os.environ, {
        "M7_MODEL_PATH": os.path.join(os.path.dirname(__file__), "test_resources", "Sentiment-M7.keras"),
        "LOOKUP_TABLE_PATH": os.path.join(os.path.dirname(__file__),"test_resources", "lookup_table.json"),
        "MODEL_VOCAB_SIZE": "10000",
        "MODEL_NUM_OOV_BUCKETS": "1000"
    })
    def test_load_model(self):
        importlib.reload(config)
        model = SentimentModel()
        self.assertIsNotNone(model.get_model(), 'Error! Expected model to be not None')


if __name__ == '__main__':
    unittest.main()
