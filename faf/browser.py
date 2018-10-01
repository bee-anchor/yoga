from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import random
from time import sleep, time

from faf.context import CONTEXT
from faf.helpers import Locator
from faf import waitables


class Browser(object):

    def __init__(self, driver=CONTEXT.driver):
        self.driver = driver

    def exit_handler(self):
        self.driver.quit()

    def navigate_to(self, url):
        self.driver.get(url)

    def click(self, locator: Locator):
        try:
            self.driver.find_element(*locator).click()
        except StaleElementReferenceException:
            sleep(0.5)
            self.driver.find_element(*locator).click()

    def click_random(self, locator: Locator):
        random.choice(self.driver.find_elements(*locator)).click()

    def retrying_click(self, locator: Locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(waitables.successful_click(locator))

    def get_element(self, locator: Locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator: Locator):
        return self.driver.find_elements(*locator)

    def get_element_text(self, locator: Locator):
        return self.driver.find_element(*locator).text

    def get_element_with_text(self, locator: Locator, text):
        elements = self.driver.find_elements(*locator)
        for elem in elements:
            if elem.text == text:
                return elem
        raise NoSuchElementException(f'Unable to find element with selector of {locator.selector} and text of {text}')

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

    def wait_until_exists_any(self, locators, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            waitables.visibility_of_any_element_located(locators)
        )

    def wait_until_exists_with_text(self, locator: Locator, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            waitables.element_to_be_present_with_text(locator, text)
        )

    def wait_until_exists_with_regex(self, locator: Locator, regex, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            waitables.element_to_be_present_with_regex(locator, regex)
        )

    def wait_until_not_exists(self, locator: Locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.invisibility_of_element_located(locator)
        )

    def exists(self, locator: Locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def displayed(self, locator: Locator):
        try:
            elem = self.driver.find_element(*locator)
            if elem.is_displayed():
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            return False
        return False

    def scroll_up_by(self, pixels):
        self.driver.execute_script(f"window.scrollTo(window.scrollX, window.scrollY - {pixels})")

    def scroll_down_by(self, pixels):
        self.driver.execute_script(f"window.scrollTo(window.scrollX, window.scrollY + {pixels})")

    def is_mobile_device(self):
        return 'platformName' in self.driver.capabilities and self.driver.capabilities['platformName'] in ['Android', 'iOS']

    def retry_until_true(self, action_func, predicate_func, timeout=10):
        current_time = time()
        until_time = current_time + timeout
        while time() < until_time:
            sleep(0.5)
            if not predicate_func():
                action_func()
            else:
                return
        raise TimeoutError("timeout waiting for predicate to become true")
