import tensorflow_datasets as tfds
import tensorflow as tf


def create_train_test_val(info: tfds.core.DatasetInfo, datasets, validation_fraction=0.2, shuffle=10000,
                          reshuffle=False):
    train_data, test_data = datasets["train"], datasets["test"]
    num_train = int(info.splits["train"].num_examples * (1 - validation_fraction))

    shuffled_train_data = train_data.shuffle(shuffle, reshuffle_each_iteration=reshuffle)
    training_data = shuffled_train_data.take(num_train)
    validation_data = shuffled_train_data.skip(num_train)
    return training_data, test_data, validation_data


def get_labels(data: tf.data.Dataset):
    return [text.numpy() for text, label in data]


def get_text_lengths(data: tf.data.Dataset):
    return [len(text.numpy().decode('utf-8')) for text, _ in data]


from collections import Counter


class LookupTableCreator:

    def __init__(self):
        self._counter = None
        self._tabel = None

    def assign_vocabs_to_counter(self, data: tf.data.Dataset, batch_size=32):
        self._counter = Counter()
        for X_batch, y_batch in data.batch(batch_size):
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
