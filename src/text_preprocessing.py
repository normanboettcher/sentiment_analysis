import tensorflow as tf
import nltk
from nltk.corpus import stopwords


class ReviewPreprocessor:

    def __init__(self, vocab_size, num_oov_buckets, lookup_table, default_value=b"0", batch_size=32, maxlen=200):
        self._vocab_size = vocab_size
        self._num_oov_buckets = num_oov_buckets
        self._batch_size = batch_size
        self._maxlen = maxlen
        self._lookup_table = lookup_table
        self._default_value = default_value

    def remove_stop_words(self, x_batch):
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        return tf.ragged.boolean_mask(x_batch, ~tf.reduce_any(x_batch[..., None] == list(stop_words), axis=-1))

    def preprocess(self, x_batch, y_batch, replace_characters=b"[^a-zA-Z0-9.,?!']"):
        x_batch = tf.strings.lower(x_batch)
        # replace <br /> with spaces
        x_batch = self.replace_with_spaces(x_batch, b"<br\\s*/?>")
        # replace any characters other than letters with spaces
        x_batch = self.replace_with_spaces(x_batch, replace_characters)
        x_batch = tf.strings.split(x_batch)
        return x_batch, y_batch

    def replace_with_spaces(self, x_batch, replace):
        return tf.strings.regex_replace(x_batch, replace, b" ")

    def to_tensor(self, x_batch):
        return x_batch.to_tensor(default_value=self._default_value)

    def encode_words(self, x_batch, y_batch):
        encoded = self._lookup_table.lookup(x_batch)
        return tf.cast(encoded, tf.int32), y_batch

    def pad_sequences_fn(self, x_batch, y_batch):
        x_batch = x_batch[:, :self._maxlen]
        padding = [[0,0 ], [0, self._maxlen - tf.shape(x_batch)[1]]]
        x_padded = tf.pad(x_batch, padding, constant_values=0)
        return x_padded, y_batch

    def prepare_data_set(self, data):
        dataset = data.map(self.preprocess)
        dataset = dataset.map(self.encode_words)
        dataset = dataset.batch(self._batch_size)
        dataset = dataset.map(self.pad_sequences_fn)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        return dataset
