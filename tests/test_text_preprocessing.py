import unittest
from numpy.ma.testutils import assert_array_equal, assert_equal
from src.text_preprocessing import ReviewPreprocessor
import tensorflow as tf


class ReviewPreprocessorTest(unittest.TestCase):
    def test_to_tensor(self):
        # Does not need a table
        preprocessor = ReviewPreprocessor(2, 5, None)
        reviews = tf.RaggedTensor.from_row_lengths(values=[b'This', b'is', b'a', b'text', b'another', b'text'],
                                                   row_lengths=[4, 2])
        dense_tensor = preprocessor.to_tensor(reviews)
        assert_array_equal(dense_tensor.numpy(), [[b'This', b'is', b'a', b'text'], [b'another', b'text', b'0', b'0']])

    def test_encode_words(self):
        keys = tf.constant([b"<pad>", b"review", b"just"])
        values = tf.constant([0, 1, 2], dtype=tf.int64)
        table = tf.lookup.StaticVocabularyTable(tf.lookup.KeyValueTensorInitializer(keys, values), 1)
        review = tf.data.Dataset.from_tensor_slices(([[b'just', b'a', b'review', b'<pad>', b'<pad>']], [1]))
        preprocessor = ReviewPreprocessor(2, 5, table)

        for x_batch, y_batch in review.batch(1).take(1):
            encoded_x, encoded_y = preprocessor.encode_words(x_batch, y_batch)
            tf.debugging.assert_equal(y_batch, encoded_y, message="Label-Tensor for y not correct")
            tf.debugging.assert_equal(tf.constant([2, 3, 1, 0, 0], dtype=tf.int32), encoded_x,
                                      message='Encoded Tensor for review not correct')

    def test_pad_sequences_fn(self):
        import numpy as np
        # Does not need a table
        preprocessor = ReviewPreprocessor(2, 5, None, maxlen=7)
        sentences = tf.constant([[2, 3, 1, 0, 0]])
        labels = tf.constant([1])

        padded_x, y = preprocessor.pad_sequences_fn(sentences, labels)
        print(f'x_batch.numpy(): {sentences.numpy()}')
        expected_padded = np.array([[2, 3, 1, 0, 0, 0, 0]], dtype=np.int32)
        tf.debugging.assert_equal(padded_x, tf.convert_to_tensor(expected_padded),
                                  message='Padded sequences are incorrect')

        self.assertEqual(padded_x.dtype, tf.int32, "Padded tensor dtype is not tf.int32")
        self.assertEqual(y.dtype, tf.int32, "Label tensor dtype is not tf.int32")

        self.assertEqual(padded_x.shape, (1, 7), "Padded tensor shape is incorrect")
        self.assertEqual(y.shape, (1,), "Label tensor shape is incorrect")

        tf.debugging.assert_equal(labels, y, message="Labels have been changed")


class TestPrepareDataset(unittest.TestCase):
    @classmethod
    def setUp(cls):
        # Create dummy table
        keys = tf.constant([b"0", b"review", b"just", b"great"])
        values = tf.constant([0, 1, 2, 3], dtype=tf.int64)
        cls._vocab_table = tf.lookup.StaticVocabularyTable(
            tf.lookup.KeyValueTensorInitializer(keys, values),
            num_oov_buckets=1
        )
        cls._maxlen = 5
        cls._preprocessor = ReviewPreprocessor(2, 1, cls._vocab_table, maxlen=cls._maxlen, batch_size=1)

        cls._x_batch = [
            b"just a review",
            b"great movie",
            b"review was just okay",
            b"This sentence about movie is just great and really long"
        ]
        cls._y_batch = [1, 0, 1, 0]
        cls._dataset = tf.data.Dataset.from_tensor_slices((cls._x_batch, cls._y_batch))

    def test_pipeline_compatibility(self):
        prepared = self._preprocessor.prepare_data_set(self._dataset)

        for x_batch, y_batch in prepared.take(4):
            print(f"x_batch: {x_batch}")
            self.assertEqual(1, x_batch.shape[0])
            self.assertEqual(self._maxlen, x_batch.shape[1])
            self.assertEqual(x_batch.dtype, tf.int32)
            self.assertEqual(y_batch.dtype, tf.int32)

    def test_fit_compatibility(self):
        prepared = self._preprocessor.prepare_data_set(self._dataset)
        # Simple Test-Model
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=5, output_dim=16, mask_zero=True),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

        history = model.fit(prepared, validation_data=prepared, epochs=1)
        self.assertIn("accuracy", history.history)


if __name__ == '__main__':
    unittest.main()
