from logging import getLogger

import tensorflow as tf
from prometheus_client import Summary
from sentiment_model.text_preprocessing import ReviewPreprocessor

from sentiment_model.review_learn import Attention

logger = getLogger("SentimentModel")

LOAD_MODEL_TIME = Summary('load_model_processing_time', 'Time spent loading the Model')
PREPROCESSING_TIME = Summary('review_preprocessing_time', 'Time spent preprocessing the review for prediction')


class SentimentModel:
    def __init__(self, model_path, preprocessor: ReviewPreprocessor):
        self._model_path = model_path
        self._model = self._load_model()
        self._preprocessor = preprocessor

    @LOAD_MODEL_TIME.time()
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
            encoded_review = self.prepare_data(review)
            prediction = self._model.predict(encoded_review)[0]
            sentiment = self.get_sentiment_from_prediction(prediction)
            return {"sentiment": sentiment}
        except Exception as e:
            logger.exception(f"Prediction failed due to an unexpected error: {e}.")
            return {"error": "An unexpected error occurred. Please try again later."}

    @PREPROCESSING_TIME.time()
    def prepare_data(self, review: str):
        return self._preprocessor.prepare_data_set(review)

    def get_sentiment_from_prediction(self, proba):
        if proba >= 0.5:
            logger.debug(f"returning positive sentiment for probability: [{proba}]")
            return "positive"
        logger.debug(f"returning negative sentiment for probability: [{proba}]")
        return "negative"
