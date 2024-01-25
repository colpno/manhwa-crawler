import os
from selenium.webdriver.remote.webelement import WebElement
from helpers.function import extract_file_from_url


def download_image(image_element: WebElement, url: str, storage_path: str):
    file = extract_file_from_url(url)
    path = os.path.join(storage_path, file)

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    with open(path, 'xb') as file:
        file.write(image_element.screenshot_as_png)

    return path
