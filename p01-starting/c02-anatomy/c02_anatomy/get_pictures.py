import json
import os

import requests
from requests import exceptions as requests_exceptions

from c02_anatomy.ensure_directory_exists import ensure_directory_exists


def write_img_to_file(content, target_file):
    with open(target_file, "wb") as f:
        f.write(content)


def download_one_picture(image_url):
    image_head, image_tail = os.path.split(image_url)
    target_file = f"/tmp/images/{image_tail}"
    try:
        response = requests.get(image_url)
        write_img_to_file(response.content, target_file)
        print(f"Downloaded {image_url} to {target_file}")
    except requests_exceptions.MissingSchema:
        print(f"{image_url} appears to be an invalid URL.")
    except requests_exceptions.ConnectionError:
        print(f"Could not connect to {image_url}.")


def read_launches_json(path_to_launches_json):
    with open(path_to_launches_json) as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
    return image_urls


def _get_pictures():
    ensure_directory_exists("/tmp/images")
    # Download all pictures in launches.json
    image_urls = read_launches_json("/tmp/launches.json")
    for image_url in image_urls:
        download_one_picture(image_url)
