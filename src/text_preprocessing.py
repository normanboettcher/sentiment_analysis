import tensorflow as tf
import nltk
from nltk.corpus import stopwords
from src.review_learn import LookupTableCreator


class ReviewPreprocessor:

    def __init__(self, vocab_size, num_oov_buckets, batch_size=32, maxlen=200):
        self._vocab_size = vocab_size
        self._num_oov_buckets = num_oov_buckets
        self._batch_size = batch_size
        self._maxlen = maxlen

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

    def encode_words(self, x_batch, y_batch, table):
        return table.lookup(x_batch), y_batch

    def pad_sequences_fn(self, x_batch, y_batch):
        x_padded = tf.keras.preprocessing.sequence.pad_sequences(x_batch.numpy(), maxlen=self._maxlen, padding='post')
        return tf.convert_to_tensor(x_padded, dtype=tf.int32), y_batch

    def prepare_data_set(self, data):
        table_creator = LookupTableCreator()
        lookup_table = table_creator.create_lookup_table(data, self._vocab_size, self._num_oov_buckets,
                                                         self._batch_size)

        dataset = data.map(lambda x, y: self.encode_words(x, y, lookup_table))
        dataset = dataset.map(lambda x, y: tf.py_function(
            func=self.pad_sequences_fn,
            inp=[x, y],
            Tout=(tf.int32, tf.int32)
        ),
                              num_parallel_calls=tf.data.AUTOTUNE)
        dataset = dataset.batch(self._batch_size)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        return dataset
