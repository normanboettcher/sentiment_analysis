import unittest

from model_api.model import SentimentModel


class TestSentimentModel(unittest.TestCase):
    def test_load_model(self):
        model = SentimentModel()
        self.assertIsNotNone(model.get_model(), 'Error! Expected model to be not None')


if __name__ == '__main__':
    unittest.main()
