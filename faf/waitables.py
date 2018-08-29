from selenium.common.exceptions import NoSuchElementException
from time import sleep
import logging

"""
 * Pre-made actions webdriver can wait for
"""

logger = logging.getLogger(__name__)

class successful_click(object):
    """ An expectation for checking that an element is present on the DOM
    of a page. This does not necessarily mean that the element is visible.
    locator - used to find the element
    returns the WebElement once it is located
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
