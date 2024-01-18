import subprocess
import os
import time

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as DriverConditions
from selenium.webdriver.support.ui import WebDriverWait as DriverWait


def wait_displayed(driver: ChromeWebDriver, xpath: str, int=3):
    try:
        DriverWait(driver, int).until(
            DriverConditions.presence_of_element_located(
                locator=(By.XPATH, xpath))
        )
    except:
        pass


def is_displayed(driver: ChromeWebDriver, xpath: str, int=3):
    try:
        webElement = DriverWait(driver, int).until(
            DriverConditions.presence_of_element_located(
                locator=(By.XPATH, xpath))
        )
        return True if webElement != None else False
    except:
        return False


def re_run():
    running_dir = os.path.abspath(f"{__file__}/../../../")
    env_dir = os.path.abspath(f"{__file__}/../../../../env/bin/activate")
    crawl_command = f'source {env_dir} && cd {running_dir} && bash run.sh'
    subprocess.run(crawl_command, shell=False)


def enable_vpn(driver: ChromeWebDriver):
    indexPage = 'chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html'

    driver.get(indexPage)

    time.sleep(5)

    try:
        driver.switch_to.window(driver.window_handles[0])

        wait_displayed(driver, "//div[@id='ConnectionButton']")

        if is_displayed(driver, "//div[@id='ConnectionButton']") == True:
            driver.find_element(By.ID, "ConnectionButton").click()

            wait_displayed(
                driver, "//div[@id='ConnectionButton']/span[contains(text(), 'Stop')]")

            if is_displayed(driver, "//div[@id='ConnectionButton']/span[contains(text(), 'Stop')]") == True:
                return driver
            else:
                re_run()
        else:
            re_run()
    except:
        pass
