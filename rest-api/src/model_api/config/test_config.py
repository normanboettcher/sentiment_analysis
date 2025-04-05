import os


class TestConfig:
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tests', 'test_resources',
                              'Sentiment-M7.keras')
    LOOKUP_TABLE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tests', 'test_resources',
                                     'lookup_table.json')
    VOCAB_SIZE = '10000'
    NUM_OOV_BUCKETS = '1000'
