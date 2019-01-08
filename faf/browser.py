from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import random
from functools import wraps
from time import sleep, time

from faf.context import CONTEXT
from faf.helpers import Locator
from faf import waitables


def handle_staleness(retry_pause=0.5):
    def staleness_decorator(func):
        @wraps(func)
        def func_wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except StaleElementReferenceException:
                sleep(retry_pause)
                return func(*args, **kwargs)
        return func_wrapped
    return staleness_decorator


class WaitUntil(object):

    @staticmethod
    def exists(locator: Locator, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator),
            f"Element with {locator.find_method} of '{locator.selector}' does not exist"
        )

    @staticmethod
    def not_exists(locator: Locator, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.invisibility_of_element_located(locator),
            f"Element with {locator.find_method} of'{locator.selector}' exists, but should not"
        )

    @staticmethod
    def exists_any(locators, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            waitables.visibility_of_any_element_located(locators),
            f"No element can be found to match any of the selectors '{locators}'"
        )

    @staticmethod
    def not_exists_any(locators, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            waitables.visibility_of_any_element_located(locators),
            f"At least one element with {locator.find_method} of '{locators}' exists, but should not"
        )

    @staticmethod
    def exists_with_text(locator: Locator, text, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            waitables.element_to_be_present_with_text(locator, text),
            f"Element with {locator.find_method} of '{locator.selector}' and text of '{text}' does not exist"
        )

    @staticmethod
    def not_exists_with_text(locator: Locator, text, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            waitables.element_to_be_present_with_text(locator, text),
            f"Element with {locator.find_method} of '{locator.selector}' and text of '{text}' exists, but should not"
        )

    @staticmethod
    def exists_with_regex(locator: Locator, regex, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            waitables.element_to_be_present_with_regex(locator, regex),
            f"Element with {locator.find_method} of '{locator.selector}' and text matching regex '{regex}' does not exist"
        )

    @staticmethod
    def not_exists_with_regex(locator: Locator, regex, timeout=10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            waitables.element_to_be_present_with_regex(locator, regex),
            f"Element with {locator.find_method} of '{locator.selector}' and text matching regex '{regex}' exists, but should not"
        )


class Browser(object):

    def _get_driver(self):
        return CONTEXT.driver

    driver = property(_get_driver)
    wait_until = WaitUntil()

    def exit_handler(self):
        self.driver.quit()

    def refresh(self):
        self.driver.refresh()

    def navigate_to(self, url):
        self.driver.get(url)

    def page_title(self):
        return self.driver.title

    @handle_staleness()
    def wait_for_and_click(self, locator: Locator):
        self.wait_until.exists(locator)
        self.driver.find_element(*locator).click()

    @handle_staleness()
    def click(self, locator: Locator):
        self.driver.find_element(*locator).click()

    @handle_staleness()
    def click_element_with_text(self, locator: Locator, text):
        self.get_element_with_text(locator, text).click()

    def click_random(self, locator: Locator):
        random.choice(self.driver.find_elements(*locator)).click()

    def retrying_click(self, locator: Locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(waitables.successful_click(locator))

    @handle_staleness()
    def get_element(self, locator: Locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator: Locator):
        return self.driver.find_elements(*locator)

    @handle_staleness()
    def get_element_text(self, locator: Locator):
        return self.driver.find_element(*locator).text

    @handle_staleness()
    def get_element_value(self, locator: Locator):
        return self.driver.find_element(*locator).get_attribute('value')

    @handle_staleness()
    def get_element_inner_html(self, locator: Locator):
        return self.driver.find_element(*locator).get_attribute('innerHTML')

    @handle_staleness()
    def get_element_classes(self, locator: Locator):
        classes = self.driver.find_element(*locator).get_attribute('class')
        return classes.split()

    def get_element_with_text(self, locator: Locator, text):
        elements = self.driver.find_elements(*locator)
        for elem in elements:
            if elem.text == text:
                return elem
        raise NoSuchElementException(f'Unable to find element with {locator.find_method} of {locator.selector} and text of {text}')

    def get_element_location(self, locator: Locator):
        elem = self.get_element(locator)
        return elem.location

    @handle_staleness()
    def fill_txtbox(self, locator: Locator, text):
        self.driver.find_element(*locator).clear()
        self.driver.find_element(*locator).send_keys(text)

    def switch_to_frame(self, locator: Locator):
        self.driver.switch_to.frame(self.driver.find_element(*locator))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def exists(self, locator: Locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def exists_with_text(self, locator: Locator, text):
        try:
            elements = self.driver.find_elements(*locator)
            for elem in elements:
                if elem.text == text:
                    return True
        except (NoSuchElementException, StaleElementReferenceException):
            pass
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

    def scroll_y_to(self, loc):
        self.driver.execute_script(f"window.scrollTo(window.scrollX, {loc})")

    def is_mobile_device(self):
        return 'platformName' in self.driver.capabilities and self.driver.capabilities['platformName'] in ['Android', 'iOS']

    def is_safari(self):
        return 'browserName' in self.driver.capabilities and self.driver.capabilities['browserName'] in ['Safari', 'safari']

    @staticmethod
    def retry_until_true(action_func, predicate_func, timeout=10):
        start_time = time()
        action_func()
        while time() < start_time + timeout:
            sleep(0.5)
            try:
                if not predicate_func():
                    action_func()
                else:
                    return
            except:
                continue
        raise TimeoutError("timeout waiting for predicate to become true")

    @staticmethod
    def retry_until_no_exceptions(action_func, failure_action_func, catch_exceptions, timeout=10):
        start_time = time()
        while time() < start_time + timeout:
            try:
                action_func()
                return
            except catch_exceptions:
                sleep(0.5)
                failure_action_func()
                continue
        action_func()

    @staticmethod
    def wait_for(condition_function, timeout=10):
        start_time = time()
        while time() < start_time + timeout:
            try:
                if condition_function():
                    return True
            except:
                continue
            else:
                sleep(0.1)
        raise TimeoutError(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout=timeout).until(expected_conditions.staleness_of(old_page))

