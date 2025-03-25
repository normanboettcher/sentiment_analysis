import tensorflow as tf
import numpy as np

import nltk
from nltk.corpus import stopwords


def create_train_test_val(datasets, validation_fraction=0.2, shuffle=10000,
                          reshuffle=False, num_samples=25000):
    train_data, test_data = datasets["train"], datasets["test"]
    num_train = int(num_samples * (1 - validation_fraction))

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


def preprocess(x_batch, y_batch, replace_characters=b"[^a-zA-Z0-9.,?!']", maxlen=200, use_words=True):
    x_batch = tf.strings.lower(x_batch)
    if use_words is False:
        x_batch = tf.strings.substr(x_batch, 0, maxlen)


    # replace <br /> with spaces
    x_batch = tf.strings.regex_replace(x_batch, b"<br\\s*/?>", b" ")
    # replace any characters other than letters with spaces
    x_batch = tf.strings.regex_replace(x_batch, replace_characters, b" ")
    x_batch = tf.strings.split(x_batch)
    x_batch = x_batch[:, :maxlen]
    return x_batch.to_tensor(default_value=b"0"), y_batch


def remove_stop_words(x_batch):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    return tf.ragged.boolean_mask(x_batch, ~tf.reduce_any(x_batch[..., None] == list(stop_words), axis=-1))
