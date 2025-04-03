from logging import getLogger

import tensorflow as tf
from sentiment_model.lookup_table_creator import LookupTableCreator
from sentiment_model.text_preprocessing import ReviewPreprocessor

import model_api.config as config
from sentiment_model.review_learn import Attention

logger = getLogger("SentimentModel")


class SentimentModel:
    def __init__(self):
        self._config = config.load_config()
        self._model = self._load_model()

    def _load_model(self):
        model_path = self._config["MODEL_PATH"]
        try:
            return tf.keras.models.load_model(
                model_path, custom_objects={"Attention": Attention}
            )
        except FileNotFoundError:
            raise Exception(f"Model not found at {model_path}")

    def get_model(self):
        return self._model

    def predict(self, review):
        if not review:
            logger.error("Empty review detected. Returning with error.")
            return {"error": "Review text is empty."}

        try:
            lookup_table = self._get_lookup_table()
            preprocessor = ReviewPreprocessor(
                lookup_table=lookup_table,
                vocab_size=self._config["VOCAB_SIZE"],
                num_oov_buckets=self._config["NUM_OOV_BUCKETS"],
            )
            # preprocess logic needs dummy y, because funcitons are designed for inputs like x_batch, y_batch
            dummy_y = [10]
            review = tf.data.Dataset.from_tensor_slices(([review], dummy_y))
            encoded_review = preprocessor.prepare_data_set(review)
            prediction = self._model.predict(encoded_review)[0]
            sentiment = self.get_sentiment_from_prediction(prediction)
            return {"sentiment": sentiment}
        except RuntimeError as e:
            return {"error": str(e)}
        except Exception:
            logger.exception("Prediction failed due to an unexpected error.")
            return {"error": "An unexpected error occurred. Please try again later."}

    def _get_lookup_table(self):
        table_path = self._config["LOOKUP_TABLE_PATH"]
        try:
            table_creator = LookupTableCreator()
            return table_creator.read_from_path(table_path)
        except Exception as e:
            logger.exception(
                f"An error occurred reading LookupTable from {table_path}."
            )
            raise RuntimeError(f"Error reading lookup table: {e}")

    def get_sentiment_from_prediction(self, proba):
        if proba >= 0.5:
            return 'positive'
        return 'negative'
