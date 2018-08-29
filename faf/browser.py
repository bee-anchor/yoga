from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
import random

import logging

from faf.driver import DRIVER
from faf.helpers import Locator
from faf.waitables import successful_click

logger = logging.getLogger(__name__)


class Browser(object):

    def __init__(self, driver=DRIVER):
        self.driver = driver

    def exit_handler(self):
        self.driver.quit()

    def navigate_to(self, url):
        self.driver.get(url)

    def click(self, locator: Locator):
        self.driver.find_element(*locator).click()

    def click_random(self, locator: Locator):
        random.choice(self.driver.find_elements(*locator)).click()

    def get_element(self, locator: Locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator: Locator):
        return self.driver.find_elements(*locator)

    def fill_txtbox(self, locator: Locator, text):
        self.driver.find_element(*locator).clear()
        self.driver.find_element(*locator).send_keys(text)

    def switch_to_frame(self, locator: Locator):
        self.driver.switch_to.frame(self.driver.find_element(*locator))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def wait_until_exists(self, locator: Locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def wait_until_not_exists(self, locator: Locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.invisibility_of_element_located(locator)
        )

    def retrying_click(self, locator: Locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(successful_click(locator))

    def exists(self, locator: Locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
