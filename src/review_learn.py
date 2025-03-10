import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np


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


def load_glove_embeddings(filepath, word_index, vocab_size=20000, embed_size=100, num_oov_buckets=1000):
    """
    Lädt vortrainierte GloVe-Embeddings und erstellt eine Matrix für unser Vokabular.
    """
    embeddings_index = {}

    # GloVe-Datei Zeile für Zeile einlesen
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]  # Erstes Element ist das Wort
            vector = np.asarray(values[1:], dtype='float32')  # Rest ist der Vektor
            embeddings_index[word] = vector

    # Embedding-Matrix für unser Vokabular erstellen
    embedding_matrix = np.zeros((vocab_size + num_oov_buckets, embed_size))
    oov_embedding = np.random.uniform(-0.1, 0.1, (num_oov_buckets, embed_size))
    for word, i in word_index.items():
        if i < vocab_size:
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector  # Falls das Wort existiert, Vektor speichern
        elif i < vocab_size + num_oov_buckets:
            embedding_matrix[i] = oov_embedding[i - vocab_size]
    return embedding_matrix


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
