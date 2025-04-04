import os
import unittest

from model_api.model.model import SentimentModel


class TestSentimentModel(unittest.TestCase):
    def test_load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), 'test_resources', 'Sentiment-M7.keras')
        lookup_table_path = os.path.join(os.path.dirname(__file__), 'test_resources', 'lookup_table.json')
        vocab_size = 10000
        num_oov_buckets = 1000
        model = SentimentModel(model_path, vocab_size, lookup_table_path, num_oov_buckets)
        self.assertIsNotNone(model.get_model(), 'Error! Expected model to be not None')


if __name__ == '__main__':
    unittest.main()
