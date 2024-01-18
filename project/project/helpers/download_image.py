import os
import validators as validators
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from urllib.request import urlopen
import base64


# url: contains filename. Ex: https://.../name.jpg
def download_image(driver: WebDriver, url: str, xpath: str, storage_path: str):
    if not (validators.url(url)):
        raise ValueError('Invalid trailer link')

    driver.implicitly_wait(1)

    driver.get(url)

    driver.implicitly_wait(10)

    url_contains_filename = driver.find_element(By.XPATH, xpath + '/@src')
    with urlopen(url_contains_filename) as url:
        f = url.read()
        image = base64.b64encode(f).decode("utf-8")

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    with open(os.path.join(storage_path, filename), 'wb') as file:
        file.write(url_contains_filename.screenshot_as_png)
