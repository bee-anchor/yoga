from contextlib import contextmanager
from typing import Union, Callable, Any, Tuple
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import random
from functools import wraps
from time import sleep, time

from yoga.context import CONTEXT
from yoga.helpers import Locator
from yoga import waitables
from .wait_until import WaitUntil

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


class Browser(object):

    def _get_driver(self) -> Union[WebDriver, AppiumWebDriver]:
        return CONTEXT.driver

    driver = property(_get_driver)
    wait_until = WaitUntil()

    def exit_handler(self):
        self.driver.quit()

    def current_url(self):
        return self.driver.current_url

    def refresh(self):
        self.driver.refresh()

    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def navigate_to(self, url: str):
        self.driver.get(url)

    def page_title(self):
        return self.driver.title

    @handle_staleness()
    def wait_for_and_click(self, locator: Locator):
        self.wait_until.visible(locator)
        self.driver.find_element(*locator).click()

    # some button clicks don't work properly in iOS (very very slow, or not at all), use this instead :)
    def js_click_elem(self, element):
        self.driver.execute_script('return arguments[0].click()', element)

    def js_click(self, locator: Locator):
        element = self.get_element(locator)
        self.js_click_elem(element)

    @handle_staleness()
    def click(self, locator: Locator):
        self.driver.find_element(*locator).click()

    @handle_staleness()
    def click_element_with_text(self, locator: Locator, text: str):
        self.get_element_with_text(locator, text).click()

    def click_random(self, locator: Locator):
        random.choice(self.driver.find_elements(*locator)).click()

    def retrying_click(self, locator: Locator, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(waitables.successful_click(locator))

    @handle_staleness()
    def select_item_by_index(self, locator: Locator, index):
        select = Select(self.get_element(locator))
        select.select_by_index(index)

    @handle_staleness()
    def select_item_by_text(self, locator: Locator, text):
        select = Select(self.get_element(locator))
        select.select_by_visible_text(text)

    @handle_staleness()
    def select_item_by_value(self, locator: Locator, value):
        select = Select(self.get_element(locator))
        select.select_by_value(value)

    @handle_staleness()
    def get_element(self, locator: Locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator: Locator):
        return self.driver.find_elements(*locator)

    @handle_staleness()
    def get_element_text(self, locator: Locator):
        return self.driver.find_element(*locator).text

    @handle_staleness()
    def get_element_text_ignoring_hidden_state(self, locator: Locator):
        return self.driver.find_element(*locator).get_attribute('textContent')

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

    def get_element_with_text(self, locator: Locator, text: str):
        elements = self.driver.find_elements(*locator)
        for elem in elements:
            if elem.text == text:
                return elem
        raise NoSuchElementException(
            f'Unable to find element with {locator.find_method} of {locator.selector} and text of {text}')

    def get_element_location(self, locator: Locator):
        elem = self.get_element(locator)
        return elem.location

    @handle_staleness()
    def fill_txtbox(self, locator: Locator, text: str):
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

    def exists_with_text(self, locator: Locator, text: str):
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

    def scroll_up_by(self, pixels: int):
        self.driver.execute_script(f"window.scrollTo(window.scrollX, window.scrollY - {pixels})")

    def scroll_down_by(self, pixels: int):
        self.driver.execute_script(f"window.scrollTo(window.scrollX, window.scrollY + {pixels})")

    def scroll_y_to(self, loc: int):
        self.driver.execute_script(f"window.scrollTo(window.scrollX, {loc})")

    def is_mobile_device(self):
        return 'platformName' in self.driver.capabilities and self.driver.capabilities['platformName'] in ['Android',
                                                                                                           'iOS']

    def is_ios_device(self):
        return 'platformName' in self.driver.capabilities and self.driver.capabilities['platformName'] == 'iOS'

    def is_android_device(self):
        return 'platformName' in self.driver.capabilities and self.driver.capabilities['platformName'] == 'Android'

    def is_safari(self):
        return 'browserName' in self.driver.capabilities and self.driver.capabilities['browserName'] in ['Safari',
                                                                                                         'safari']

    def delete_cookie(self, cookie_name: str):
        self.driver.delete_cookie(cookie_name)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    @staticmethod
    def retry_until_true(action_func: Callable[[], Any],
                         predicate_func: Callable[[], bool], timeout: int = 10):
        start_time = time()
        action_func()
        while time() < start_time + timeout:
            sleep(0.5)
            try:
                if not predicate_func():
                    action_func()
                else:
                    return
            except Exception:
                continue
        raise TimeoutError("timeout waiting for predicate to become true")

    @staticmethod
    def retry_until_no_exceptions(action_func: Callable[[], Any], failure_action_func: Callable[[], Any],
                                  catch_exceptions: Union[Exception, Tuple[Exception]], timeout: int = 10):
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
    def wait_for(condition_function: Callable[[], bool], timeout: int = 10):
        start_time = time()
        while time() < start_time + timeout:
            try:
                if condition_function():
                    return True
            except Exception:
                continue
            else:
                sleep(0.1)
        raise TimeoutError(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    @contextmanager
    def wait_for_page_load(self, timeout: int = 10):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout=timeout).until(expected_conditions.staleness_of(old_page))
