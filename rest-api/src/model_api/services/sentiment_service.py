from flask import current_app, Config

from model_api.model.model import SentimentModel


def get_sentiment(review: str, config: Config) -> dict:
    model_path = config['MODEL_PATH']
    vocab_size = config['VOCAB_SIZE']
    lookup_table_path = config['LOOKUP_TABLE_PATH']
    num_oov_buckets = config['NUM_OOV_BUCKETS']
    model = SentimentModel(model_path, vocab_size, lookup_table_path, num_oov_buckets)
    return model.predict(review)
