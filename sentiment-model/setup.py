from attr.filters import exclude
from setuptools import setup
from setuptools.config.expand import find_packages

setup(
    name="sentiment_model",
    version="2.0",
    packages=find_packages(include=["sentiment_model"]),
)
