import sys
import os
import random
import datetime
from helpers.selenium_driver_setup import SeleniumSetup
from selenium.webdriver.common.by import By

PROJECT_DIR = os.path.abspath(f"{__file__}/../../project")
SCRIPT_FILE = f'{PROJECT_DIR}/run.sh'
JSON_FILE = f"{PROJECT_DIR}/data/manhwa.json"
MAX_REST_TIME = 15
MIN_REST_TIME = 5
CRAWLING_TIME = 90
ARGUMENT_LIST = sys.argv[1:]
COLOR_PURPLE = "\\033[1;35m"
COLOR_GREEN = "\\033[0;32m"
COLOR_NORMAL = "\\033[0m"

url = ARGUMENT_LIST[1] if len(ARGUMENT_LIST) > 0 else 'https://acomics.net/'

driver = SeleniumSetup.configure_chrome_driver()
driver.get(url)

elements = driver.find_elements(By.XPATH, '//div[@class="novel-cover"]/a')
lines = ["#!/bin/bash\n", f"source {PROJECT_DIR}/../env/bin/activate\n"]

with open(SCRIPT_FILE, 'w') as f:
    elements_len = len(elements)-1
    for index, element in enumerate(elements):
        link = element.get_attribute('href')
        lines.append(f'\nscrapy crawl manhwa -a start_url="{link}"\n')

        if index != elements_len:
            time = random.randint(MIN_REST_TIME, MAX_REST_TIME)
            remaining = elements_len-index
            remaining_time = remaining * (CRAWLING_TIME+MAX_REST_TIME-MIN_REST_TIME)
            estimate = str(datetime.timedelta(seconds=remaining_time))

            lines.append(f'echo -e "{COLOR_PURPLE}Remaining: {remaining} - Estimate: {estimate}"\n')
            lines.append(f"sleep {time}s\n")

    lines.append(f"\nsed -i 's/]\[/,/g' {JSON_FILE}\n")

    lines.append(f"if grep -nzoP '\[\\n\\n\]' {JSON_FILE}; then\n")
    lines.append(f"\tcode {JSON_FILE}\n")
    lines.append("fi\n\n")

    lines.append( f'echo -e "{COLOR_GREEN}  _______         _____       __    __     ________ {COLOR_NORMAL}"\n')
    lines.append( f'echo -e "{COLOR_GREEN} |   __   \     /       \    |  \  |  |   |  ______|{COLOR_NORMAL}"\n')
    lines.append( f'echo -e "{COLOR_GREEN} |  |  \   |   |   ___   |   |   \ |  |   | |______ {COLOR_NORMAL}"\n')
    lines.append( f'echo -e "{COLOR_GREEN} |  |  |   |   |  |   |  |   |    \|  |   |  ______|{COLOR_NORMAL}"\n')
    lines.append( f'echo -e "{COLOR_GREEN} |  |__/   |   |   ‾‾‾   |   |  | \   |   | |______ {COLOR_NORMAL}"\n')
    lines.append( f'echo -e "{COLOR_GREEN} |_______ /     \ _____ /    |__|  \__|   |________|{COLOR_NORMAL}"')

    f.writelines(lines)
    f.close()

driver.quit()

print("Done")
