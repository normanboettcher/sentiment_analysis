from sentiment_model.text_preprocessing import ReviewPreprocessor
import tensorflow as tf
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"