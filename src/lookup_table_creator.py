from collections import Counter

from src.review_learn import preprocess
import tensorflow as tf


class LookupTableCreator:

    def __init__(self):
        self._counter = None

    def assign_vocabs_to_counter(self, data: tf.data.Dataset, batch_size=32):
        self._counter = Counter()
        for X_batch, y_batch in data.batch(batch_size).map(preprocess):
            for review in X_batch.numpy():
                self._counter.update(review.tolist())

    def get_counter(self):
        return self._counter

    def prepare_truncated_vocabs(self, vocab_size, vocabs):
        return [word for word, _ in vocabs[:vocab_size]]

    def create_lookup_table(self, data, vocab_size, num_oov_buckets, batch_size=32):
        self.assign_vocabs_to_counter(data, batch_size)
        trunc_vocabs = self.prepare_truncated_vocabs(vocab_size, self._counter.most_common())
        words = tf.constant(trunc_vocabs)
        word_ids = tf.range(len(trunc_vocabs), dtype=tf.int64)
        vocab_init = tf.lookup.KeyValueTensorInitializer(words, word_ids)

        return tf.lookup.StaticVocabularyTable(vocab_init, num_oov_buckets)
