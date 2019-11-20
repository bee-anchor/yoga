from selenium import webdriver
from appium import webdriver as appium_webdriver
import atexit
from yoga.context import CONTEXT
from yoga.remote.sauce_helper import SauceHelper
from yoga.capabilities import Capabilities


class Driver(object):

    def __init__(self, args):
        self.args = args

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

        elif self.args.execution == 'appium_remote_real':
            driver = self.__appium_remote_real_driver()
            self.__name_saucelabs_job(driver.session_id)

        elif self.args.execution == 'grid_local':
            driver = self.__grid_local_driver()

        elif self.args.execution == 'grid_remote':
            driver = self.__grid_remote_driver()

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
            atexit.unregister(CONTEXT.driver.quit)

        driver = self.get_driver()
        driver.set_page_load_timeout(30)
        CONTEXT.update_driver(driver)

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
        desired_capabilities = Capabilities(self.args).get_local_capabilities()
        return appium_webdriver.Remote(command_executor, desired_capabilities)

    def __remote_driver(self, driver_type):
        url = CONTEXT.config['remote_service']['remote_url']

        if driver_type == 'selenium' or driver_type == 'appium':
            username = CONTEXT.config['remote_service']['username']
            access_key = CONTEXT.config['remote_service']['access_key']
            command_executor = f"http://{username}:{access_key}@{url}"

        desired_capabilities = Capabilities(self.args).get_remote_capabilities()
        desired_capabilities['idleTimeout'] = CONTEXT.config['remote_service']['job_timeout']

        if driver_type == 'appium_real':
            desired_capabilities['testobject_api_key'] = CONTEXT.config['remote_service']['testobject_api_key']

        if 'tunnel' in self.args and self.args.tunnel:
            desired_capabilities['tunnelIdentifier'] = self.args.tunnel

        self.capabilities = desired_capabilities

        if driver_type == 'selenium':
            return webdriver.Remote(command_executor, desired_capabilities)
        elif driver_type == 'appium':
            return appium_webdriver.Remote(command_executor, desired_capabilities)
        elif driver_type == 'appium_real':
            command_executor = f"http://{url}"
            return appium_webdriver.Remote(command_executor, desired_capabilities)

    def __selenium_remote_driver(self):
        return self.__remote_driver('selenium')

    def __appium_remote_driver(self):
        return self.__remote_driver('appium')

    def __appium_remote_real_driver(self):
        return self.__remote_driver('appium_real')

    def __grid_local_driver(self):
        command_executor = "http://localhost:4444/wd/hub"
        desired_capabilities = {
            'browserName': self.args.browser
        }
        return webdriver.Remote(command_executor, desired_capabilities)

    def __grid_remote_driver(self):
        command_executor = CONTEXT.config['remote_grid']['remote_url']
        desired_capabilities = {
            'browserName': self.args.browser
        }
        return webdriver.Remote(command_executor, desired_capabilities)

    def __name_saucelabs_job(self, session_id):
        caps = Capabilities(self.args).get_formatted_remote_capabilities()
        name = f"{CONTEXT.config['application']['name']} - {caps}"
        SauceHelper().update_job_name(session_id, name)
