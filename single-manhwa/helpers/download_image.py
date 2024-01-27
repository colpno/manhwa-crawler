import os
import shutil
import requests
from selenium.webdriver.remote.webelement import WebElement
from helpers.function import extract_file_from_url


def download_image(image_element: WebElement, url: str, storage_path: str, driver):
    file = extract_file_from_url(url)
    path = os.path.join(storage_path, file)
    response = requests.get(url, stream=True)

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    with open(path, 'wb') as f:
        shutil.copyfileobj(response.raw, f)

    del response

    return path
