from collections import Counter
from review_learn import preprocess
import tensorflow as tf


class LookupTableCreator:

    def __init__(self):
        self._counter = None
        self._words = None
        self._word_ids = None

    def assign_vocabs_to_counter(self, data: tf.data.Dataset, batch_size=32):
        self._counter = Counter()
        for X_batch, y_batch in data.batch(batch_size).map(preprocess):
            for review in X_batch.numpy():
                self._counter.update(review.tolist())

    def read_from_path(self, path):
        import json
        # load lookup table from json
        with open(path, 'r') as file:
            loaded_dict = json.load(file)
        # make string keys to byte strings\n
        lookup_dict_bytes = {key.encode('utf-8'): value for key, value in loaded_dict.items()}
        vocabs = tf.constant(list(lookup_dict_bytes.keys()))
        self._word_ids = tf.constant(list(lookup_dict_bytes.values()), dtype=tf.int64)
        self._words = tf.lookup.KeyValueTensorInitializer(vocabs, self._word_ids)
        table = tf.lookup.StaticVocabularyTable(self._words, num_oov_buckets=1000)
        return table

    def get_counter(self):
        return self._counter

    def prepare_truncated_vocabs(self, vocab_size, vocabs):
        return [word for word, _ in vocabs[:vocab_size]]

    def get_words(self):
        return self._words

    def get_word_ids(self):
        return self._word_ids

    def create_lookup_table(self, data, vocab_size, num_oov_buckets, batch_size=32):
        self.assign_vocabs_to_counter(data, batch_size)
        trunc_vocabs = self.prepare_truncated_vocabs(vocab_size, self._counter.most_common())
        self._words = tf.constant(trunc_vocabs)
        self._word_ids = tf.range(len(trunc_vocabs), dtype=tf.int64)
        vocab_init = tf.lookup.KeyValueTensorInitializer(self._words, self._word_ids)

        return tf.lookup.StaticVocabularyTable(vocab_init, num_oov_buckets)
