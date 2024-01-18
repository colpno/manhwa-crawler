import logging
import os
from project.helpers.enable_vpn import enable_vpn
from fake_useragent import FakeUserAgent
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

ua = FakeUserAgent()

resource_dir = os.path.abspath(os.getcwd() + '/project/resources')


class SeleniumSetup():
    def configure_chrome_driver():
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        LOGGER.setLevel(logging.WARNING)

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument("--no-sandbox")
        options.add_argument(f"--user-agent={ua.random}")
        options.add_extension(resource_dir + '/touch_vpn.crx')

        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(options, service)

        enable_vpn(driver)

        return driver
