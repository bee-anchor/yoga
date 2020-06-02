from typing import List, AnyStr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from yoga.context import CONTEXT
from yoga.helpers import Locator
from yoga import waitables

class WaitUntil(object):

    @staticmethod
    def title_is(title: str, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.title_is(title),
            f"Page title was not '{title}' as expected"
        )

    @staticmethod
    def title_contains(title: str, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.title_is(title),
            f"Page title did not contain '{title}' as expected"
        )

    @staticmethod
    def url_is(url: str, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.url_to_be(url),
            f"Current url was not '{url}' as expected"
        )

    @staticmethod
    def url_contains(url: str, timeout: int = 10):
        return WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.url_contains(url),
            f"Current url did not contain '{url}' as expected"
        )

    @staticmethod
    def visible(locator: Locator, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator),
            f"Element with {locator.find_method} of '{locator.selector}' is not visible"
        )

    @staticmethod
    def exists(locator: Locator, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.presence_of_element_located(locator),
            f"Element with {locator.find_method} of '{locator.selector}' does not exist"
        )

    @staticmethod
    def not_exists(locator: Locator, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.invisibility_of_element_located(locator),
            f"Element with {locator.find_method} of'{locator.selector}' exists, but should not"
        )

    @staticmethod
    def clickable(locator: Locator, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            expected_conditions.element_to_be_clickable(locator),
            f"Element with {locator.find_method} of'{locator.selector}' is not clickable"
        )

    @staticmethod
    def exists_any(locators: List[Locator], timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            waitables.presence_of_any_element_located(locators),
            f"No element can be found to match any of the selectors '{locators}'"
        )

    @staticmethod
    def not_exists_any(locators: List[Locator], timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            waitables.presence_of_any_element_located(locators),
            f"At least one element matching the locators is present'{locators}'"
        )

    @staticmethod
    def visible_any(locators: List[Locator], timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            waitables.visibility_of_any_element_located(locators),
            f"No element can be found to match any of the selectors '{locators}'"
        )

    @staticmethod
    def not_visible_any(locators: List[Locator], timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            waitables.visibility_of_any_element_located(locators),
            f"At least one element matching the locators is present'{locators}'"
        )

    @staticmethod
    def exists_with_text(locator: Locator, text: str, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            waitables.element_to_be_present_with_text(locator, text),
            f"Element with {locator.find_method} of '{locator.selector}' and text of '{text}' does not exist"
        )

    @staticmethod
    def not_exists_with_text(locator: Locator, text: str, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            waitables.element_to_be_present_with_text(locator, text),
            f"Element with {locator.find_method} of '{locator.selector}' and text of '{text}' exists, but should not"
        )

    @staticmethod
    def exists_with_regex(locator: Locator, regex: AnyStr, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until(
            waitables.element_to_be_present_with_regex(locator, regex),
            f"Element with {locator.find_method} of '{locator.selector}'"
            f"and text matching regex '{regex}' does not exist"
        )

    @staticmethod
    def not_exists_with_regex(locator: Locator, regex: AnyStr, timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            waitables.element_to_be_present_with_regex(locator, regex),
            f"Element with {locator.find_method} of '{locator.selector}'"
            f"and text matching regex '{regex}' exists, but should not"
        )

    @staticmethod
    def alert_is_present(timeout: int = 10):
        WebDriverWait(CONTEXT.driver, timeout).until_not(
            expected_conditions.alert_is_present(),
            f"No alert is present"
        )