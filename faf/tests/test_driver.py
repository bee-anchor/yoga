import pytest
from unittest.mock import MagicMock, patch
import faf.driver
from argparse import Namespace
import configparser


class TestDriver:

    webdriver_chrome = MagicMock()
    webdriver_firefox = MagicMock()
    webdriver_ie = MagicMock()
    webdriver_safari = MagicMock()
    webdriver_edge = MagicMock()
    webdriver_remote = MagicMock()
    appium_remote = MagicMock()

    faf.driver.webdriver.Chrome = webdriver_chrome
    faf.driver.webdriver.Firefox = webdriver_firefox
    faf.driver.webdriver.Ie = webdriver_ie
    faf.driver.webdriver.Safari = webdriver_safari
    faf.driver.webdriver.Edge = webdriver_edge
    faf.driver.webdriver.Remote = webdriver_remote
    faf.driver.appium_webdriver.Remote = appium_remote

    @pytest.mark.parametrize('browser,mock', [
        ('chrome', webdriver_chrome),
        ('firefox', webdriver_firefox),
        ('internet explorer', webdriver_ie),
        ('safari', webdriver_safari),
        ('edge', webdriver_edge)
    ])
    def test_create_local_selenium_driver(self, browser, mock):
        args = Namespace(execution='selenium_local', browser=browser)

        faf.driver.Driver(args).get_driver()

        mock.assert_called_once()

    def test_create_grid_driver(self):
        args = Namespace(execution='grid_local', browser='chrome')
        desired_capabilities = {
            'browserName': 'chrome'
        }

        faf.driver.Driver(args).get_driver()

        self.webdriver_remote.assert_called_with("http://localhost:4444/wd/hub", desired_capabilities)

    def test_create_remote_selenium_driver(self):
        test_config = configparser.ConfigParser()
        test_config.add_section('remote_service')
        test_config.set('remote_service', 'selenium_url', 'selenium.com')
        test_config.set('remote_service', 'username', 'test')
        test_config.set('remote_service', 'access_key', 'test')
        test_config.add_section('application')
        test_config.set('application', 'name', 'test')
        faf.driver.CONTEXT.config = test_config
        args = Namespace(execution='selenium_remote', capability='windows10.chrome')
        desired_capabilities = {
            'browserName': 'chrome',
            'platform': 'Windows 10',
            'version': '68.0'
        }

        with patch.object(faf.driver.Driver, '_Driver__set_saucelabs_job_name') as patched_set_saucelabs_name:
            faf.driver.Driver(args).get_driver()
            patched_set_saucelabs_name.assert_called_once()

        self.webdriver_remote.assert_called_with("http://test:test@selenium.com", desired_capabilities)

    def test_create_remote_appium_driver(self):
        test_config = configparser.ConfigParser()
        test_config.add_section('remote_service')
        test_config.set('remote_service', 'appium_url', 'appium.com')
        test_config.set('remote_service', 'username', 'test')
        test_config.set('remote_service', 'access_key', 'test')
        test_config.add_section('application')
        test_config.set('application', 'name', 'test')
        faf.driver.CONTEXT.config = test_config
        args = Namespace(execution='appium_remote', capability='android6')
        desired_capabilities = {
            'appiumVersion': '1.8.1',
            'deviceName': 'Android Emulator',
            'deviceOrientation': 'portrait',
            'browserName': 'Chrome',
            'platformVersion': '6.0',
            'platformName': 'Android'
        }

        with patch.object(faf.driver.Driver, '_Driver__set_saucelabs_job_name') as patched_set_saucelabs_name:
            faf.driver.Driver(args).get_driver()
            patched_set_saucelabs_name.assert_called_once()

        self.appium_remote.assert_called_with("http://test:test@appium.com", desired_capabilities)

    def test_raises_error_when_unrecognised_execution_argument(self):
        args = Namespace(execution='unknown')

        with pytest.raises(RuntimeError, match='Unable to set driver, unrecognised execution type: unknown'):
            faf.driver.Driver(args).get_driver()

    def test_raises_error_when_remote_and_unknown_capability(self):
        test_config = configparser.ConfigParser()
        test_config.add_section('remote_service')
        test_config.set('remote_service', 'selenium_url', 'appium.com')
        test_config.set('remote_service', 'username', 'test')
        test_config.set('remote_service', 'access_key', 'test')
        faf.driver.CONTEXT.config = test_config
        args = Namespace(execution='selenium_remote', capability='unknown')

        with pytest.raises(KeyError, match='Remote capabilities config does not have section for selection: unknown'):
            faf.driver.Driver(args).get_driver()


