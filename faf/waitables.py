from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re

"""
 * Pre-made actions webdriver can wait for
"""


class successful_click(object):
    """ An expectation for checking that a click to an element was successful.
    element - locator used to find the element
    returns if the click was successful
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            sleep(1)
            driver.find_element(*self.locator).click()
            return True
        except NoSuchElementException:
            return False


class element_to_be_present_with_text(object):
    """ An expectation for checking if and element exists with the given
    text.
    locator, text
    """
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        for elem in elements:
            if elem.text == self.text:
                return True
        return False


class element_to_be_present_with_regex(object):
    """ An expectation for checking if and element exists with text that
    matches the given regex.
    locator, text
    """
    def __init__(self, locator, regex):
        self.locator = locator
        self.regex = regex

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        for elem in elements:
            if re.search(self.regex, elem.text):
                return True
        return False
