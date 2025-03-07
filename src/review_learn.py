import tensorflow_datasets as tfds
import tensorflow as tf
def create_train_test_val(info: tfds.core.DatasetInfo, datasets, validation_fraction=0.2):
    train_data, test_data = datasets["train"], datasets["test"]
    num_train = int(info.splits["train"].num_examples * (1 - validation_fraction))

    shuffled_train_data = train_data.shuffle(10000, reshuffle_each_iteration=False)
    training_data = shuffled_train_data.take(num_train)
    validation_data = shuffled_train_data.skip(num_train)
    return training_data, test_data, validation_data

def get_labels(data: tf.data.Dataset):
    return [text.numpy() for text, label in data]

def get_text_lengths(data: tf.data.Dataset):
    return [len(text.numpy().decode('utf-8')) for text, _ in data]