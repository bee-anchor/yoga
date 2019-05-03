from argparse import Namespace
from typing import Union
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from configparser import ConfigParser


class __Context(object):

    def __init__(self):
        self.args: Namespace = None
        self.config: ConfigParser = None
        self.driver: Union[AppiumWebDriver, WebDriver] = None

    def update_args(self, args):
        self.args = args

    def update_config(self, config):
        self.config = config

    def update_driver(self, driver):
        self.driver = driver

    def clear_context(self):
        self.args = None
        self.config = None
        self.driver = None


CONTEXT = __Context()
