#!/usr/bin/env python3
from urllib.parse import quote_plus
import requests

BASE_URL = 'https://gretel.hum.uu.nl/api/src/router.php/'


def parse_sentence(sentence: str) -> str:
    url = BASE_URL + 'parse_sentence/' + quote_plus(sentence)
    response = requests.get(url)
    response.raise_for_status()
    return response.text
