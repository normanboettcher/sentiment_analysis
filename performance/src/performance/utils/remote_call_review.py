import json
import sys
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from itertools import islice
import csv
import requests
import subprocess
from requests import RequestException

from performance.utils.metric_scraper import MetricScraper


class Seperator(Enum):
    KOMMA = ','
    SEMICOLON = ';'
    TAB = 't'


def parse_separator(value: str) -> Seperator | None:
    return next((s for s in Seperator if s.value == value), None)


def extract_reviews(n_reviews: str, col_sep: str, file_path: str) -> list[str]:
    if not col_sep:
        raise ValueError('Please provide a valid separator')
    separator = parse_separator(col_sep)
    if separator is None:
        raise ValueError(f'Could not work with the separator {col_sep}. Please provide a valid separator.')
    if not file_path:
        raise ValueError(f'The path {file_path} is not a valid path.')
    if n_reviews is None:
        raise ValueError(f'Please provide a valid number for the amount of reviews you want.')
    try:
        reviews_amount = int(n_reviews)
    except (ValueError, TypeError) as error:
        raise ValueError(f'Could not parse {n_reviews} to a number: {error}')
    with open(file_path, mode='r', encoding='utf-8') as file:
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


def send_review(review: str):
    payload = json.dumps({"review": review})
    node_port, node_ip = get_node_port()
    headers = {"content-type": "application/json"}
    try:
        requests.post(url=f'http://{node_ip}:{node_port}/api/predict',
                      data=payload, headers=headers)
        return True
    except RequestException as error:
        print(f'Error occured calling the REST-API for review {review}', error)
        return False


def fire_reviews(review_list: list[str], parallel=False):
    count = 0
    if parallel:
        print("Sending reviews in parallel")
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(send_review, review_list))
            for i, success in enumerate(results):
                if success:
                    count += 1
                    if count % 50 == 0:
                        print(f"sent {count} reviews successfully")
    else:
        print("Sending reviews sequential")
        for i, review in enumerate(review_list):
            success = send_review(review)
            if success:
                count += 1
                if count % 50 == 0:
                    print(f"sent {count} reviews successfully")


if __name__ == '__main__':
    wanted_reviews, sep, path = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        if sys.argv[4] == "True":
            parallel = True
        else:
            parallel = False
    except (ValueError, TypeError) as err:
        raise ValueError(f"Error occurred trying to parse {sys.argv} to boolean", err)

    print(f"call rest api with number {wanted_reviews}, file: {path} and separator {sep}")
    reviews = extract_reviews(wanted_reviews, sep, path)
    print(f"Extracted {len(reviews)} reviews.")
    if len(reviews) != int(wanted_reviews):
        print("Die Anzahl an extrahierten Reviews stimmt nicht mit der gewünschten Anzahl überein")
        sys.exit(1)
    fire_reviews(reviews, parallel)

    metric_scraper = MetricScraper()
    metric_scraper.get_avg_request_time_total()
