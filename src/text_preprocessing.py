import tensorflow as tf
import nltk
from nltk.corpus import stopwords


class ReviewPreprocessor:

    def remove_stop_words(self, x_batch):
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        return tf.ragged.boolean_mask(x_batch, ~tf.reduce_any(x_batch[..., None] == list(stop_words), axis=-1))

    def preprocess(self, x_batch, y_batch, default_value=b"0", replace_characters=b"[^a-zA-Z0-9.,?!']"):
        x_batch = tf.strings.lower(x_batch)
        # x_batch = tf.strings.substr(x_batch, 0, 600)
        # replace <br /> with spaces
        x_batch = self.replace_with_spaces(x_batch, b"<br\\s*/?>")
        # replace any characters other than letters with spaces
        x_batch = self.replace_with_spaces(x_batch, replace_characters)
        x_batch = tf.strings.split(x_batch)
        x_batch = self.to_tensor(x_batch, default=default_value)
        return x_batch, y_batch

    def replace_with_spaces(self, x_batch, replace):
        return tf.string.regex.replace(x_batch, replace, b" ")

    def to_tensor(self, x_batch, default=b"0"):
        return x_batch.to_tensor(default_value=default)