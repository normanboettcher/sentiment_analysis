import unittest
from numpy.ma.testutils import assert_array_equal, assert_equal
from src.text_preprocessing import ReviewPreprocessor
import tensorflow as tf


class ReviewPreprocessorTest(unittest.TestCase):

    def test_to_tensor(self):
        preprocessor = ReviewPreprocessor(2, 5)
        reviews = tf.RaggedTensor.from_row_lengths(values=[b'This', b'is', b'a', b'text', b'another', b'text'],
                                                   row_lengths=[4, 2])
        dense_tensor =preprocessor.to_tensor(reviews)
        assert_array_equal(dense_tensor.numpy(), [[b'This', b'is', b'a', b'text'], [b'another', b'text', b'0', b'0']])

    def test_encode_words(self):
        preprocessor = ReviewPreprocessor(2, 5)
        keys = tf.constant([b"<pad>", b"review", b"just"])
        values = tf.constant([0, 1, 2], dtype=tf.int64)
        table = tf.lookup.StaticVocabularyTable(tf.lookup.KeyValueTensorInitializer(keys, values), 1)
        review = tf.data.Dataset.from_tensor_slices(([[b'just', b'a', b'review', b'<pad>', b'<pad>']], [1]))
        for x_batch, y_batch in review.batch(1).take(1):
            encoded_x, encoded_y = preprocessor.encode_words(x_batch, y_batch, table)
            tf.debugging.assert_equal(y_batch, encoded_y, message="Label-Tensor for y not correct")
            tf.debugging.assert_equal(tf.constant([2, 3, 1, 0, 0], dtype=tf.int64), encoded_x,
                                      message='Encoded Tensor for review not correct')

    def test_pad_sequences_fn(self):
        import numpy as np
        preprocessor = ReviewPreprocessor(2, 5, maxlen=7)
        sentences = tf.constant([[2, 3, 1, 0, 0]])
        labels = tf.constant([1])

        padded_x, y = preprocessor.pad_sequences_fn(sentences, labels)
        print(f'x_batch.numpy(): {sentences.numpy()}')
        expected_padded = np.array([[2, 3, 1, 0, 0, 0, 0]], dtype=np.int32)
        tf.debugging.assert_equal(padded_x, tf.convert_to_tensor(expected_padded), message='Padded sequences are incorrect')

        self.assertEqual(padded_x.dtype, tf.int32, "Padded tensor dtype is not tf.int32")
        self.assertEqual(y.dtype, tf.int32, "Label tensor dtype is not tf.int32")

        self.assertEqual(padded_x.shape, (1, 7), "Padded tensor shape is incorrect")
        self.assertEqual(y.shape, (1,), "Label tensor shape is incorrect")

        tf.debugging.assert_equal(labels, y, message="Labels have been changed")

    class TestPrepareDataset(unittest.TestCase):
        def test_(self):
            self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
