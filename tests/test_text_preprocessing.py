import unittest
from numpy.ma.testutils import assert_array_equal, assert_equal
from src.text_preprocessing import ReviewPreprocessor
import tensorflow as tf
from unittest.mock import patch


class ReviewPreprocessorTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls._preprocessor = ReviewPreprocessor()

    def test_to_tensor(self):
        reviews = tf.RaggedTensor.from_row_lengths(values=[b'This', b'is', b'a', b'text', b'another', b'text'],
                                                   row_lengths=[4, 2])
        dense_tensor = self._preprocessor.to_tensor(reviews)
        assert_array_equal(dense_tensor.numpy(), [[b'This', b'is', b'a', b'text'], [b'another', b'text', b'0', b'0']])

    def test_encode_words(self):
        keys = tf.constant([b"<pad>", b"review", b"just"])
        values = tf.constant([0, 1, 2], dtype=tf.int64)
        table = tf.lookup.StaticVocabularyTable(tf.lookup.KeyValueTensorInitializer(keys, values), 1)
        review = tf.data.Dataset.from_tensor_slices(([[b'just', b'a', b'review', b'<pad>', b'<pad>']], [1]))
        for x_batch, y_batch in review.batch(1).take(1):
            encoded_x, encoded_y = self._preprocessor.encode_words(x_batch, y_batch, table)
            tf.debugging.assert_equal(y_batch, encoded_y, message="Label-Tensor for y not correct")
            tf.debugging.assert_equal(tf.constant([2, 3, 1, 0, 0], dtype=tf.int64), encoded_x, message='Encoded Tensor for review not correct')


if __name__ == '__main__':
    unittest.main()
