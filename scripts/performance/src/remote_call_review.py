import json
import sys
from enum import Enum
from itertools import islice
import csv
from typing import Any

import requests
import subprocess

from requests import RequestException


class Seperator(Enum):
    KOMMA = ','
    SEMICOLON = ';'
    TAB = 't'


def parse_separator(value: str) -> Seperator | None:
    return next((s for s in Seperator if s.value == value), None)


def extract_reviews(n: int, sep: str, path: str) -> list[str]:
    if not sep:
        raise ValueError('Please provide a valid separator')
    separator = parse_separator(sep)
    if separator is None:
        raise ValueError(f'Could not work with the separator {sep}. Please provide a valid separator.')
    if not path:
        raise ValueError(f'The path {path} is not a valid path.')
    if n is None:
        raise ValueError(f'Please provide a valid number for the amount of reviews you want.')
    try:
        reviews_amount = int(n)
    except (ValueError, TypeError) as err:
        raise ValueError(f'Could not parse {n} to a number: {err}')

    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=separator.value, quotechar='"')
        return [row[0] for row in islice(reader, reviews_amount)]


def get_node_port() -> tuple[str | None, str | None]:
    try:
        result = subprocess.run(
            ["kubectl", "get", "svc", "model-api-service", "-n", "sentiment-app-dev", "-o", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        service_data = json.loads(result.stdout)
        ports = service_data["spec"]["ports"]
        node_port = ports[0]["nodePort"] if ports else None

        node_result = subprocess.run(
            ["kubectl", "get", "nodes", "-o", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        nodes_data = json.loads(node_result.stdout)
        node_ip = nodes_data["items"][0]["status"]["addresses"]
        external_ip = next((addr["address"] for addr in node_ip if addr["type"] in ["ExternalIP", "InternalIP"]), None)

        return str(node_port) if node_ip is not None else None, str(external_ip) if external_ip is not None else None
    except subprocess.CalledProcessError as e:
        print(f'Error executing kubectl:', e.stderr)
        raise
    except (KeyError, IndexError) as e:
        print(f'Error occured parsing the kubectl output', e)
        raise


def fire_review(reviews: list[str]):
    for review in reviews:
        payload = json.dumps({"review": review})
        node_port, node_ip = get_node_port()
        headers = {'content-type': 'application/json'}
        try:
            requests.post(url=f'http://{node_ip}:{node_port}/api/predict',
                          data=payload, headers=headers)
        except RequestException as err:
            print(f'error occured calling the REST-API for review {review}', err)


if __name__ == '__main__':
    n, sep, path = sys.argv[1], sys.argv[2], sys.argv[3]
    reviews = extract_reviews(n, sep, path)
    fire_review(reviews)
