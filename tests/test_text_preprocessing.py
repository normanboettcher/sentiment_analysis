import unittest
from numpy.ma.testutils import assert_array_equal
from src.text_preprocessing import ReviewPreprocessor
import tensorflow as tf

class ReviewPreprocessorTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls._preprocessor = ReviewPreprocessor()

    def test_to_tensor(self):
        reviews = tf.RaggedTensor.from_row_lengths(values=[b'This', b'is', b'a', b'text', b'another', b'text'],
                                                   row_lengths=[4,2])
        dense_tensor = self._preprocessor.to_tensor(reviews)
        assert_array_equal(dense_tensor.numpy(), [[b'This', b'is', b'a', b'text'], [b'another', b'text', b'0', b'0']])

if __name__ == '__main__':
    unittest.main()
