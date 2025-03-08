import tensorflow as tf

class ReviewPreprocessor:
    def __init__(self, train_data: tf.data.Dataset, test_data: tf.data.Dataset, validation_data: tf.data.Dataset):
        self._train_data = train_data
        self._test_data = test_data
        self._validation_data = validation_data
