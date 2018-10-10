from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import re

"""
 * Pre-made actions webdriver can wait for
"""


class successful_click(object):
    """ An expectation for checking that a click to an element was successful.
    locator - used to find the element
    returns if the click was successful
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            driver.find_element(*self.locator).click()
            return True
        except NoSuchElementException:
            sleep(0.5)
            return False


class element_to_be_present_with_text(object):
    """ An expectation for checking if and element exists with the given
    text.
    locator - used to find the element
    text - what must match the elements text
    """
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        try:
            elements = driver.find_elements(*self.locator)
            for elem in elements:
                if elem.text == self.text:
                    return True
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        return False


class element_to_be_present_with_regex(object):
    """ An expectation for checking if and element exists with text that
    matches the given regex.
    locator - used to find the elements
    regex - expession to match to element text
    """
    def __init__(self, locator, regex):
        self.locator = locator
        self.regex = regex

    def __call__(self, driver):
        try:
            elements = driver.find_elements(*self.locator)
            for elem in elements:
                if re.search(self.regex, elem.text):
                    return True
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        return False


class visibility_of_any_element_located(object):
    """ An expectation for checking if any given element exists on the page

    """
    def __init__(self, locators):
        self.locators = locators

    def __call__(self, driver):
        for locator in self.locators:
            try:
                elem = driver.find_element(*locator)
                if elem.is_displayed():
                    return True
            except (NoSuchElementException, StaleElementReferenceException):
                continue
        return False
