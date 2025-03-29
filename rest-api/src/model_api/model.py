import tensorflow as tf
import model_api.config as config


class SentimentModel:
    def __init__(self):
        self._model = self._load_model()

    def _load_model(self):
        return tf.keras.models.load_model(config.MODEL_PATH, custom_objects={'Attention': Attention})

    def get_model(self):
        return self._model


# Attention Layer Definition
from keras.saving import register_keras_serializable


@register_keras_serializable(package="CustomLayers")
class Attention(tf.keras.layers.Layer):
    def __init__(self, name=None, **kwargs):
        super(Attention, self).__init__(name=name, **kwargs)

    def call(self, inputs):
        # Energie-Werte berechnen (Dot-Produkt der Inputs mit sich selbst)
        score = tf.matmul(inputs, inputs, transpose_b=True)

        # Softmax über die Scores zur Normalisierung
        attention_weights = tf.nn.softmax(score, axis=-1)

        # Kontextvektor als gewichtete Summe der Eingaben
        context_vector = tf.matmul(attention_weights, inputs)

        return context_vector

    def get_config(self):
        config = super().get_config()  # Hole die Basiskonfiguration
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)
