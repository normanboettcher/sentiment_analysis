import tensorflow as tf

from src.review_learn import preprocess


class ReviewPreprocessor:

    def __init__(self, vocab_size, num_oov_buckets, lookup_table, default_value=b"0", batch_size=32, maxlen=200):
        self._vocab_size = vocab_size
        self._num_oov_buckets = num_oov_buckets
        self._batch_size = batch_size
        self._maxlen = maxlen
        self._lookup_table = lookup_table
        self._default_value = default_value

    def encode_words(self, x_batch, y_batch):
        encoded = self._lookup_table.lookup(x_batch)
        return tf.cast(encoded, tf.int32), y_batch

    def pad_sequences_fn(self, x_batch, y_batch):
        padding = [[0, 0], [0, self._maxlen - tf.shape(x_batch)[1]]]
        x_padded = tf.pad(x_batch, padding, constant_values=0)
        return x_padded, y_batch

    def prepare_data_set(self, data, use_words=True):
        dataset = data.batch(self._batch_size)
        dataset = dataset.map(lambda x,y: preprocess(x,y, maxlen=self._maxlen, use_words=use_words))
        dataset = dataset.map(self.encode_words)
        dataset = dataset.map(self.pad_sequences_fn)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        return dataset
