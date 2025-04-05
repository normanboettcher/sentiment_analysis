from logging import getLogger

import tensorflow as tf
from sentiment_model.text_preprocessing import ReviewPreprocessor

from sentiment_model.review_learn import Attention

logger = getLogger("SentimentModel")


class SentimentModel:
    def __init__(self, model_path, preprocessor: ReviewPreprocessor):
        self._model_path = model_path
        self._model = self._load_model()
        self._preprocessor = preprocessor

    def _load_model(self):
        try:
            return tf.keras.models.load_model(
                self._model_path, custom_objects={"Attention": Attention}
            )
        except FileNotFoundError:
            raise Exception(f"Model not found at {self._model_path}")

    def get_model(self):
        return self._model

    def predict(self, review):
        if not review:
            logger.error("Empty review detected. Returning with error.")
            return {"error": "Review text is empty."}
        try:
            # preprocess logic needs dummy y, because funcitons are designed for inputs like x_batch, y_batch
            dummy_y = [10]
            review = tf.data.Dataset.from_tensor_slices(([review], dummy_y))
            encoded_review = self._preprocessor.prepare_data_set(review)
            prediction = self._model.predict(encoded_review)[0]
            sentiment = self.get_sentiment_from_prediction(prediction)
            return {"sentiment": sentiment}
        except Exception:
            logger.exception("Prediction failed due to an unexpected error.")
            return {"error": "An unexpected error occurred. Please try again later."}

    def get_sentiment_from_prediction(self, proba):
        if proba >= 0.5:
            return 'positive'
        return 'negative'
