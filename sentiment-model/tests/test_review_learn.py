import unittest

from numpy.ma.testutils import assert_array_equal, assert_equal

import tensorflow as tf

from sentiment_model.lookup_table_creator import LookupTableCreator


class LookupTableCreatorTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls._creator = LookupTableCreator()
        cls._sentences = [b"hello world like you", b"hello darling"]
        cls._labels = [0, 1]

    def test_assign_vocabs(self):
        dataset = tf.data.Dataset.from_tensor_slices((self._sentences, self._labels))

        self._creator.assign_vocabs_to_counter(dataset)
        result = self._creator.get_counter().most_common()
        assert_array_equal(result[:2], [(b"hello", 2), (b"0", 2)])
        # 6 different words
        assert_equal(len(result), 6)

    def test_prepare_truncated_vocabs(self):
        vocabs = [(b"hello", 2), (b"world", 2), (b"my", 1)]
        trunc_vocabs = self._creator.prepare_truncated_vocabs(2, vocabs)
        assert_array_equal(trunc_vocabs, [b"hello", b"world"])
        assert_equal(len(trunc_vocabs), 2)

    def test_create_lookup_table(self):
        data = tf.data.Dataset.from_tensor_slices((self._sentences, self._labels))
        table = self._creator.create_lookup_table(data, 2, 3)
        sentence = tf.constant([b"hello", b"hat", b"are", b"you", b"0", b"0"])
        lookup = table.lookup(sentence)
        print(f"most_common: {self._creator.get_counter().most_common()}")
        assert_array_equal(lookup, [0, 2, 4, 3, 1, 1])


if __name__ == '__main__':
    unittest.main()
