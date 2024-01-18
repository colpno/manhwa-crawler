import re
import time

import validators
from project.helpers.selenium_driver_setup import SeleniumSetup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def check_valid_ip(ip):
    if not (validators.ipv4(ip)):
        raise ValueError('Invalid proxy address')


def check_valid_port(port):
    if not (port.isnumeric()):
        raise ValueError('Invalid proxy port')


def completeProxy(ip: str, port=80) -> str:
    check_valid_ip(ip)
    check_valid_port(port)
    return 'http://' + ip + ':' + port


def get_proxy():
    driver = SeleniumSetup.configure_chrome_driver()

    try:
        driver.get("https://www.yougetsignal.com/tools/open-ports")

        time.sleep(2)

        port = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='portNumber']"))).get_attribute('value')
        ip = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='remoteAddress']"))).get_attribute('value')

        return completeProxy(ip, port)

    except TimeoutException:
        driver.get("https://api.ipify.org/?format=json")

        json_string = driver.find_element(By.XPATH, '//body/pre/text()').get()

        ip_pattern = r'"ip":"([\d.]+)"'
        match = re.search(ip_pattern, json_string)

        if match:
            ip = match.group(1)
            return completeProxy(ip)

        raise ValueError("Something wrong with ip")

    finally:
        driver.quit()
