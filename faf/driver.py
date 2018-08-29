from selenium import webdriver
from appium import webdriver as appium_webdriver
import atexit
import configparser

DRIVER = None


def get_driver(args):
    if args.execution == 'selenium_local':
        browser_mapping = {
            'chrome': webdriver.Chrome,
            'firefox': webdriver.Firefox,
            'internet explorer': webdriver.Ie,
            'safari': webdriver.Safari,
            'edge': webdriver.Edge,
        }

        driver = browser_mapping[args.browser]()

    elif args.execution == 'selenium_remote':
        command_executor = "http://username:access_key@ondemand.saucelabs.com:80/wd/hub"
        caps = configparser.ConfigParser()
        caps.read('remote/capabilites.ini')
        desired_capabilities = caps[args.remote_capability]
        driver = webdriver.Remote(command_executor, desired_capabilities)

    elif args.execution == 'appium_local':
        command_executor = "http://localhost:4723/wd/hub"
        desired_capabilities = {

        }
        driver = appium_webdriver.Remote(command_executor, desired_capabilities)

    elif args.execution == 'appium_remote':
        command_executor = "http://username:access_key@ondemand.saucelabs.com:80/wd/hub"
        caps = configparser.ConfigParser()
        caps.read('remote/capabilites.ini')
        desired_capabilities = caps[args.remote_capability]
        driver = appium_webdriver.Remote(command_executor, desired_capabilities)

    elif args.execution == 'grid_local':
        command_executor = "http://localhost:4444/wd/hub"
        desired_capabilities = {

        }
        driver = appium_webdriver.Remote(command_executor, desired_capabilities)

    elif args.execution == 'non-ui':
        # don't set up driver if running API etc tests
        return

    else:
        raise RuntimeError(f'Unable to set driver, unrecognised execution type: {args.execution}')

    atexit.register(driver.quit)
    return driver


def set_driver(args):
    global DRIVER
    if DRIVER is not None:
        DRIVER.quit()

    DRIVER = get_driver(args)

