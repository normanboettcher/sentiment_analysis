import os
import unittest
from unittest.mock import patch

from flask import current_app

from model_api.app import create_app
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
            self.assertEqual(config['FRONTEND_HOST'], 'localhost')
            self.assertEqual(config['FRONTEND_PORT'], '5000')

    @patch.dict(os.environ, {'M7_MODEL_PATH': '/mock/',
                             'LOOKUP_TABLE_PATH': '/mock/',
                             'FRONTEND_HOST_URL': 'localhost',
                             'FRONTEND_PORT': '5000'})
    def test_app_config_prod(self):
        app = create_app(config_name="Production")


if __name__ == '__main__':
    unittest.main()
