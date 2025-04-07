from logging import getLogger

from flask import Config
from sentiment_model.lookup_table_creator import LookupTableCreator
from sentiment_model.text_preprocessing import ReviewPreprocessor
from tensorflow.python.ops.lookup_ops import StaticVocabularyTable

from model_api.model.model import SentimentModel

logger = getLogger("sentiment_service")


def get_sentiment(review: str, config: Config) -> dict:
    try:
        model_path, vocab_size, lookup_table_path, num_oov_buckets = read_env_vars(
            config
        )
        lookup_table = get_lookup_table(lookup_table_path)
        preprocessor = create_review_preprocessor(
            lookup_table, vocab_size, num_oov_buckets
        )
    except RuntimeError as e:
        logger.exception(
            f"A RuntimeError occurred creating lookup_table and ReviewPreprocessor: {e}"
        )
        return {
            "error": "An error occurred reading the lookup_table or environment variables from config!"
            " Please message your service provider."
        }
    except Exception as e:
        logger.exception(f"An unexpected Error occurred: {e}")
        return {"error": "An unexpected error occurred. Please try again later."}
    model = SentimentModel(model_path, preprocessor)
    return model.predict(review)


def read_env_vars(config: Config):
    return (
        config["MODEL_PATH"],
        config["VOCAB_SIZE"],
        config["LOOKUP_TABLE_PATH"],
        config["NUM_OOV_BUCKETS"],
    )


def get_lookup_table(lookup_table_path) -> StaticVocabularyTable:
    table_path = lookup_table_path
    try:
        table_creator = LookupTableCreator()
        return table_creator.read_from_path(table_path)
    except Exception as e:
        logger.exception(f"An error occurred reading LookupTable from {table_path}.")
        raise RuntimeError(f"Error reading lookup table: {e}")


def create_review_preprocessor(
    lookup_table, vocab_size, num_oov_buckets
) -> ReviewPreprocessor:
    return ReviewPreprocessor(
        lookup_table=lookup_table,
        vocab_size=vocab_size,
        num_oov_buckets=num_oov_buckets,
    )
