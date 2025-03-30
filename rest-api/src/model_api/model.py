from logging import getLogger

import tensorflow as tf
from sentiment_model.lookup_table_creator import LookupTableCreator
from sentiment_model.text_preprocessing import ReviewPreprocessor

import model_api.config as config
from sentiment_model.review_learn import Attention

logger = getLogger('SentimentModel')


class SentimentModel:
    def __init__(self):
        self._model = self._load_model()

    def _load_model(self):
        return tf.keras.models.load_model(config.MODEL_PATH, custom_objects={'Attention': Attention})

    def get_model(self):
        return self._model

    def predict(self, review):
        if not review:
            logger.error('Empty review detected. Returning with error.')
            return {"error": "Review text is empty."}

        try:
            table_creator = LookupTableCreator()
            table = table_creator.read_from_path(config.LOOKUP_TABLE_PATH)
        except Exception as e:
            return {"error": str(e)}

        preprocessor = ReviewPreprocessor(lookup_table=table, vocab_size=config.VOCAB_SIZE,
                                          num_oov_buckets=config.NUM_OOV_BUCKETS)
        # preprocess logic needs dummy y, because funcitons are designed for inputs like x_batch, y_batch
        dummy_y = [10]
        review = tf.data.Dataset.from_tensor_slices(([review], dummy_y))
        encoded_review = preprocessor.prepare_data_set(review)
        sentiment = self._model.predict(encoded_review)[0]
        return {"review": review, "sentiment": sentiment}
