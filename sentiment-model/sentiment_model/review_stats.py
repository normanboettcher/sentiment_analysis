import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

from review_learn import get_text_lengths, get_labels
import numpy as np


def print_stats_of_texts(data):
    return f"""
    | Average text length: {np.mean(data)} 
    | Median text length: {np.median(data)}
    | Minimum text length: {np.min(data)}
    | Maximum text length: {np.max(data)}
     """


def print_text_stats(dataset, dataset_name):
    text_lengths = get_text_lengths(dataset)
    print(f"Statistics of {dataset_name} Data: {print_stats_of_texts(text_lengths)}")


class TextStatisticUtils:
    def __init__(self, train_set: tf.data.Dataset, test_set: tf.data.Dataset, val_set: tf.data.Dataset):
        self._train_set = train_set
        self._test_set = test_set
        self._val_set = val_set

    def draw_class_dists(self):
        self._draw_subplots([get_labels(self._train_set), get_labels(self._test_set), get_labels(self._val_set)],
                            ["Training data class distribution", "Test data class distribution",
                             "Validation data class distribution"],
                            sns.countplot, kde=False, bins=None)

    def draw_text_length_dist(self):
        self._draw_subplots([get_labels(self._train_set), get_labels(self._test_set), get_labels(self._val_set)],
                            ["Distribution of text lengths (Training Data)", "Distribution of text lengths (Test Data)",
                             "Distribution of text lengths (Validation Data)"],
                            sns.histplot, kde=True, bins=30)

    def print_test_text_stats(self):
        return print_text_stats(self._test_set, 'Test')

    def print_train_text_stats(self):
        return print_text_stats(self._train_set, 'Train')

    def print_val_text_stats(self):
        return print_text_stats(self._val_set, 'Validation')

    def print_all_text_stats(self):
        self.print_train_text_stats()
        self.print_test_text_stats()
        self.print_val_text_stats()

    def print_bincount(self):
        for name, labels in [("Train", get_labels(self._train_set)),
                             ("Test", get_labels(self._test_set)),
                             ("Validation", get_labels(self._val_set))]:
            print(f"Class distribution in {name} dataset: {np.bincount(labels)}")

    def _draw_subplots(self, data_list, titles, plot_func, bins=None, kde=True):
        fig, axes = plt.subplots(1, len(data_list), figsize=(15, 5))
        if bins is not None and kde:
            for i, (data, title) in enumerate(zip(data_list, titles)):
                plot_func(data, bins=bins, kde=kde, ax=axes[i])
                axes[i].set_title(title)
        else:
            for i, (data, title) in enumerate(zip(data_list, titles)):
                plot_func(data, ax=axes[i])
                axes[i].set_title(title)

        plt.tight_layout()
        plt.show()
