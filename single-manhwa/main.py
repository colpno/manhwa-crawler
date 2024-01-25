import sys
import time
import os
import json
import random
from helpers.selenium_driver_setup import SeleniumSetup
from selenium.webdriver.common.by import By
from helpers.download_image import download_image

JSON_FILE = "data/data.json"
ARGUMENT_LIST = sys.argv[1:]
FIRST_PAGE = 1

if len(ARGUMENT_LIST) > 0:
    url = ARGUMENT_LIST[0]
else:
    raise Exception('Missing argument: link of manhwa')

driver = SeleniumSetup.configure_chrome_driver()


def get_urls():
    urls = {}

    print(f'Accessing {url}')
    driver.get(url)

    first_page_btn = driver.find_element(
        By.XPATH, '//a[@class="first_episode"]')
    total_page = int(ARGUMENT_LIST[1]) if len(ARGUMENT_LIST) > 1 else len(
        driver.find_elements(By.XPATH, '//ul[@class="chapter-list"]/li'))
    max_page = total_page + 1

    first_page_btn.click()

    for page in range(FIRST_PAGE, max_page):
        print(f'Crawling chapter {page}')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(5)

        next_btn = driver.find_element(
            By.XPATH, '//div[@class="btn-group"]/a[2]')

        elements = driver.find_elements(
            By.XPATH, '//div[@class="chapter-content"]//img')

        sources = []

        time.sleep(3)
        for element in elements:
            url = element.get_attribute('src')
            time.sleep(random.randint(0, 2))
            sources.append(url)

        urls[page] = sources

        if page != total_page:
            next_btn.click()
            time.sleep(random.randint(6, 10))
    print(urls)
    return urls


def download_contents(urls: dict):
    data = {}
    for key, value in urls.items():
        print(f'Downloading contents of chapter {key}')
        paths = []

        for url in value:
            driver.get(url)
            time.sleep(5)

            img = driver.find_elements(By.XPATH, '/html/body/*')[0]
            time.sleep(1)
            path_to_image = download_image(
                img, url, os.path.abspath(f'./data/{key}'))
            time.sleep(3)

            paths.append(path_to_image)

        data[key] = paths

    with open(JSON_FILE, 'w') as f:
        json.dump(data, f)
        f.close()


urls = get_urls()
download_contents(urls)

driver.quit()
