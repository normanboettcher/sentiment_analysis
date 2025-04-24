import os.path
import unittest
from unittest.mock import patch, MagicMock, ANY

from flask import Config

from model_api.services.sentiment_service import read_env_vars, get_lookup_table, get_sentiment


class SentimentServiceTest(unittest.TestCase):
    def setUp(self):
        self._config = Config(root_path='')
        self._config['MODEL_PATH'] = 'some/path'
        self._config['LOOKUP_TABLE_PATH'] = 'table_path'

    def test_read_env_vars_no_exception_if_model_path_none(self):
        self._config['MODEL_PATH'] = None
        module_path, table_path= read_env_vars(self._config)
        self.assertEqual(module_path, None)
        self.assertEqual(table_path, 'table_path')

    def test_get_lookup_table_success(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'test_resources', 'lookup_table.json')
        table = get_lookup_table(path)
        self.assertIsNotNone(table)

    def test_get_lookup_table_raises_runtime_error(self):
        path = 'right/here'
        with self.assertRaises(RuntimeError) as context:
            table = get_lookup_table(path)

        self.assertIn("Error reading lookup table:", str(context.exception))

    @patch('model_api.services.sentiment_service.get_lookup_table')
    def test_get_sentiment_no_lookup_table_found(self, get_lookup_table_mock):
        config = MagicMock()
        get_lookup_table_mock.side_effect = RuntimeError('my error occurred')
        result = get_sentiment('some review', config)
        # get_senitment should have catched the exception and returned an error
        self.assertIn('error', result)

    @patch('model_api.services.sentiment_service.get_lookup_table')
    @patch('model_api.services.sentiment_service.read_env_vars')
    def test_get_sentiment_value_error_raised(self, lookup_table_mock, read_env_vars_mock):
        config = MagicMock()
        lookup_table_mock.return_value = MagicMock()
        read_env_vars_mock.side_effect = ValueError('Oh No! Value Error occurred!')
        result = get_sentiment('some review', config)
        lookup_table_mock.assert_called_once_with(ANY)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'An unexpected error occurred. Please try again later.')


if __name__ == '__main__':
    unittest.main()
