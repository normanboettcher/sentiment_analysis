import unittest

from flask import Config

from model_api.services.sentiment_service import read_env_vars


class SentimentServiceTest(unittest.TestCase):
    def setUp(self):
        self._config = Config(root_path='')
        self._config['MODEL_PATH'] = 'some/path'
        self._config['VOCAB_SIZE'] = '1'
        self._config['LOOKUP_TABLE_PATH'] = 'table_path'
        self._config['NUM_OOV_BUCKETS'] = '1'

    def test_read_env_vars_no_exception_if_model_path_none(self):
        self._config['MODEL_PATH'] = None
        module_path, vocab_size, table_path, oov_buckets = read_env_vars(self._config)
        self.assertEqual(vocab_size, '1')
        self.assertEqual(oov_buckets, '1')
        self.assertEqual(module_path, None)
        self.assertEqual(table_path, 'table_path')


if __name__ == '__main__':
    unittest.main()
