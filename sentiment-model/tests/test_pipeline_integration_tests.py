import unittest

import tensorflow as tf
import tensorflow_datasets as tfds

from src.lookup_table_creator import LookupTableCreator
from src.review_learn import create_train_test_val, build_model, load_glove_embeddings
from src.text_preprocessing import ReviewPreprocessor


class PipelineIntegrationTests(unittest.TestCase):
    def test_integration_test(self):
        validation_fraction = 0.1
        batch_size = 32
        num_oov_buckets = 300
        vocab_size = 500
        max_len = 100
        # get the dataset
        datasets = tfds.load('imdb_reviews', as_supervised=True, with_info=False)
        # for integration testing use 1000 samples only
        # create train, test and validation data
        train_set, test_set, val_set = create_train_test_val(datasets, validation_fraction=validation_fraction,
                                                             shuffle=100, num_samples=1000)

        lookup_table_creator = LookupTableCreator()
        lookup_table = lookup_table_creator.create_lookup_table(train_set, vocab_size, num_oov_buckets,
                                                                batch_size=batch_size)
        # create the preprocessor und preprocess the datasets
        preprocessor = ReviewPreprocessor(vocab_size, num_oov_buckets, lookup_table, batch_size=batch_size,
                                          maxlen=max_len)
        train_data, test_data, validation_data = preprocessor.prepare_data_set(
            train_set), preprocessor.prepare_data_set(test_set), preprocessor.prepare_data_set(val_set)

        embeddings = load_glove_embeddings('../embeddings/glove.6B.100d.txt', tf.keras.datasets.imdb.get_word_index(),
                                           vocab_size=vocab_size, embed_size=100, num_oov_buckets=num_oov_buckets)
        for x_batch, y_batch in train_data.take(1):
            print(f"x_shape: {x_batch.shape}")
            print(f"y_shape {y_batch.shape}")
        # create the model and run it for 3 epochs
        model = build_model(n_hidden=1, vocab_size=vocab_size, num_oov_buckets=num_oov_buckets,
                            embedding_matrix=embeddings, embed_size=100)
        history = model.fit(train_data, validation_data=validation_data, epochs=3)
        self.assertIn("accuracy", history.history)


if __name__ == '__main__':
    unittest.main()
