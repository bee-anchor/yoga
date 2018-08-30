from selenium.common.exceptions import NoSuchElementException
from time import sleep
import logging

"""
 * Pre-made actions webdriver can wait for
"""

logger = logging.getLogger(__name__)

class successful_click(object):
    """ An expectation for checking that a click to an element was successful.
    element - locator used to find the element
    returns if the click was successful
    """

    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        try:
            sleep(1)
            driver.find_element(*self.element).click()
            return True
        except NoSuchElementException:
            logger.info(f"Element {element.selector} not yet present")
            return False
