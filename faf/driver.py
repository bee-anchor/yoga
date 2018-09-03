from selenium import webdriver
from appium import webdriver as appium_webdriver
import atexit
import os
import configparser
from faf.context import CONTEXT
from faf.remote.sauce_helper import SauceHelper


class Driver(object):

    def __init__(self, args):
        self.args = args
        self.capabilities = None

    def get_driver(self):
        if self.args.execution == 'selenium_local':
            driver = self.__selenium_local_driver()

        elif self.args.execution == 'selenium_remote':
            driver = self.__selenium_remote_driver()
            self.__name_saucelabs_job(driver.session_id)

        elif self.args.execution == 'appium_local':
            driver = self.__appium_local_driver()

        elif self.args.execution == 'appium_remote':
            driver = self.__appium_remote_driver()
            self.__name_saucelabs_job(driver.session_id)

        elif self.args.execution == 'grid_local':
            driver = self.__grid_local_driver()

        elif self.args.execution == 'non-ui':
            # don't set up driver if running API etc tests
            return
        else:
            raise RuntimeError(f'Unable to set driver, unrecognised execution type: {self.args.execution}')

        if not self.args.execution == 'non-ui':
            atexit.register(driver.quit)
        return driver

    def set_driver(self):
        if CONTEXT.driver is not None:
            CONTEXT.driver.quit()

        CONTEXT.update_driver(self.get_driver())

    def __selenium_local_driver(self):
        browser_mapping = {
            'chrome': webdriver.Chrome,
            'firefox': webdriver.Firefox,
            'internet explorer': webdriver.Ie,
            'safari': webdriver.Safari,
            'edge': webdriver.Edge,
        }

        return browser_mapping[self.args.browser]()

    def __appium_local_driver(self):
        command_executor = "http://localhost:4723/wd/hub"
        # TODO how to handle people's individual capabilities?
        desired_capabilities = {

        }
        return appium_webdriver.Remote(command_executor, desired_capabilities)

    def __remote_driver(self, driver_type):
        if driver_type == 'selenium':
            url = CONTEXT.config['remote_service']['selenium_url']
        elif driver_type == 'appium':
            url = CONTEXT.config['remote_service']['appium_url']
        username = CONTEXT.config['remote_service']['username']
        access_key = CONTEXT.config['remote_service']['access_key']
        command_executor = f"http://{username}:{access_key}@{url}"
        caps = configparser.ConfigParser()
        caps.optionxform = str
        caps_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      'remote', 'capabilities.ini')
        caps.read(caps_file_path)
        print(caps_file_path)
        print(caps.sections())
        if not caps.has_section(self.args.capability):
            raise KeyError(f'Remote capabilities config does not have section for selection: {self.args.capability}')
        desired_capabilities = dict(caps[self.args.capability])
        self.capabilities = desired_capabilities
        if driver_type == 'selenium':
            return webdriver.Remote(command_executor, desired_capabilities)
        elif driver_type == 'appium':
            return appium_webdriver.Remote(command_executor, desired_capabilities)

    def __selenium_remote_driver(self):
        return self.__remote_driver('selenium')

    def __appium_remote_driver(self):
        return self.__remote_driver('appium')

    def __grid_local_driver(self):
        command_executor = "http://localhost:4444/wd/hub"
        desired_capabilities = {
            'browserName': self.args.browser
        }
        return webdriver.Remote(command_executor, desired_capabilities)

    def __name_saucelabs_job(self, session_id):
        name = f"{CONTEXT.config['application']['name']} - {str(self.capabilities)}"
        SauceHelper().update_job_name(session_id, name)




