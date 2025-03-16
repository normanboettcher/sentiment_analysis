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


from tensorflow.keras.regularizers import l2


def build_model(n_hidden=2, embed_size=128, vocab_size=10000, num_oov_buckets=1000, dropout_rate=0.3,
                embedding_matrix=None):
    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.Embedding(input_dim=vocab_size + num_oov_buckets, output_dim=embed_size,
                                        weights=[embedding_matrix], trainable=False))
    # 1D Convolutional Layer (Extrahiert lokale Merkmale)
    model.add(tf.keras.layers.Conv1D(filters=128, kernel_size=5, activation="relu", padding="same"))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling1D(pool_size=2))
    for hidden in range(n_hidden):
        model.add(
            tf.keras.layers.Bidirectional(tf.keras.layers.GRU(128, return_sequences=True, dropout=dropout_rate)))
    model.add(tf.keras.layers.Bidirectional(tf.keras.layers.GRU(64)))
    model.add(tf.keras.layers.Dropout(dropout_rate))
    model.add(tf.keras.layers.Dense(64, activation="relu", kernel_regularizer=l2(0.001)))
    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  metrics=["accuracy"])
    return model


def preprocess(x_batch, y_batch, replace_characters=b"[^a-zA-Z0-9.,?!']", maxlen=200):
    x_batch = tf.strings.lower(x_batch)
    # replace <br /> with spaces
    x_batch = tf.strings.regex_replace(x_batch, b"<br\\s*/?>", b" ")
    # replace any characters other than letters with spaces
    x_batch = tf.strings.regex_replace(x_batch, replace_characters, b" ")
    x_batch = tf.strings.split(x_batch)
    x_batch = x_batch[:, :maxlen]
    return x_batch.to_tensor(default_value=b""), y_batch


def remove_stop_words(x_batch):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    return tf.ragged.boolean_mask(x_batch, ~tf.reduce_any(x_batch[..., None] == list(stop_words), axis=-1))
