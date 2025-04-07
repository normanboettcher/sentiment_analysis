import unittest

from flask import current_app
from .test_resources.test_config import create_test_app, TestConfig


class AppTestCase(unittest.TestCase):
    def test_app_config(self):
        app = create_test_app()
        with app.app_context():
            config = current_app.config
            self.assertIsNotNone(config)
            self.assertEqual(config['MODEL_PATH'], TestConfig.MODEL_PATH)
            self.assertEqual(config['NUM_OOV_BUCKETS'], TestConfig.NUM_OOV_BUCKETS)
            self.assertEqual(config['VOCAB_SIZE'], TestConfig.VOCAB_SIZE)
            self.assertEqual(config['LOOKUP_TABLE_PATH'], TestConfig.LOOKUP_TABLE_PATH)


if __name__ == '__main__':
    unittest.main()
