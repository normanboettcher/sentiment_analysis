import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from review_learn import get_text_lengths
import numpy as np
from review_learn import get_labels


def print_stats_of_texts(data):

    stats = """
    | Average text length: {} 
    | Median text length: {}
    | Minimum text length: {}
    | Maximum text length: {}
     """.format(np.mean(data), np.median(data), np.min(data), np.max(data))
    return stats


class TextStatisticUtils:
    def __init__(self, train_set: tf.data.Dataset, test_set: tf.data.Dataset, val_set: tf.data.Dataset):
        self.__train_set = train_set
        self.__test_set = test_set
        self.__val_set = val_set

    def draw_class_dists(self):

        train_labels = get_labels(self.__train_set)
        test_labels = get_labels(self.__test_set)
        validation_labels = get_labels(self.__val_set)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.countplot(x=train_labels, ax=axes[0])
        axes[0].set_title('Training data class distribution')

        sns.countplot(x=test_labels, ax=axes[1])
        axes[1].set_title('Test data class distribution')
        sns.countplot(x=validation_labels, ax=axes[2])
        axes[2].set_title('Validation data class distribution')

        plt.tight_layout()
        plt.show()

    def draw_text_length_dist(self):
        train_text_lengths = get_text_lengths(self.__train_set)
        test_text_lengths = get_text_lengths(self.__test_set)
        val_text_lengths = get_text_lengths(self.__val_set)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.histplot(train_text_lengths, bins=30, kde=True, ax=axes[0])
        axes[0].set_title('Distribution of text lengths (Training Data)')
        sns.histplot(test_text_lengths, bins=30, kde=True, ax=axes[1])
        axes[1].set_title('Distribution of text lengths (Test Data)')
        sns.histplot(val_text_lengths, bins=30, kde=True, ax=axes[2])
        axes[2].set_title('Distribution of text lengths (Validation Data)')

        plt.tight_layout()
        plt.show()

    def print_test_text_stats(self):
        test_text_lengths = get_text_lengths(self.__test_set)
        print(f"Statistics of Test Data: {print_stats_of_texts(test_text_lengths)}")

    def print_train_text_stats(self):
        train_text_lengths = get_text_lengths(self.__train_set)
        print(f"Statistics of Train Data: {print_stats_of_texts(train_text_lengths)}")
    def print_val_text_stats(self):
        val_text_lengths = get_text_lengths(self.__val_set)
        print(f"Statistics of Validation Data: {print_stats_of_texts(val_text_lengths)}")

    def print_all_text_stats(self):
        self.print_train_text_stats()
        self.print_test_text_stats()
        self.print_val_text_stats()

    def print_bincount(self):
        train_labels = get_labels(self.__train_set)
        val_labels = get_labels(self.__val_set)
        test_labels = get_labels(self.__test_set)

        print(f"Train-Labels: {np.bincount(train_labels)}")
        print(f"Validation-Labels: {np.bincount(val_labels)}")
        print(f"Test-Labels {np.bincount(test_labels)}")
