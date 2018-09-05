import pytest
from unittest.mock import patch
import faf.driver
from argparse import Namespace
import configparser


class TestDriver:

    @pytest.fixture(autouse=True)
    def mock_setup(self):
        self.mock_webdriver_patch = patch('faf.driver.webdriver')
        self.mock_appium_webdriver_patch = patch('faf.driver.appium_webdriver')
        self.mock_webdriver = self.mock_webdriver_patch.start()
        self.mock_appium_webdriver = self.mock_appium_webdriver_patch.start()
        yield
        self.mock_webdriver = self.mock_webdriver_patch.stop()
        self.mock_appium_webdriver = self.mock_appium_webdriver_patch.stop()

    @pytest.mark.parametrize('browser,expected_driver', [
        ('chrome', 'Chrome'),
        ('firefox', 'Firefox'),
        ('internet explorer', 'Ie'),
        ('safari', 'Safari'),
        ('edge', 'Edge')
    ])
    def test_create_local_selenium_driver(self, browser, expected_driver):
        args = Namespace(execution='selenium_local', browser=browser)

        faf.driver.Driver(args).get_driver()

        getattr(self.mock_webdriver, expected_driver).assert_called_once()

    def test_create_grid_driver(self):
        args = Namespace(execution='grid_local', browser='chrome')
        desired_capabilities = {
            'browserName': 'chrome'
        }

        faf.driver.Driver(args).get_driver()

        self.mock_webdriver.Remote.assert_called_with("http://localhost:4444/wd/hub", desired_capabilities)

    @patch('faf.driver.CONTEXT')
    def test_create_remote_selenium_driver(self, mock_context):
        test_config = configparser.ConfigParser()
        test_config.add_section('remote_service')
        test_config.set('remote_service', 'remote_url', 'selenium.com')
        test_config.set('remote_service', 'username', 'test')
        test_config.set('remote_service', 'access_key', 'test')
        test_config.add_section('application')
        test_config.set('application', 'name', 'test')
        mock_context.config = test_config
        args = Namespace(execution='selenium_remote', capability='windows10.chrome')
        desired_capabilities = {
            'browserName': 'chrome',
            'platform': 'Windows 10',
            'version': '68.0'
        }

        self.mock_webdriver.Remote.return_value.session_id = '1234'
        with patch.object(faf.driver.Driver, '_Driver__name_saucelabs_job') as patched_set_saucelabs_name:
            faf.driver.Driver(args).get_driver()
            patched_set_saucelabs_name.assert_called_with('1234')

        self.mock_webdriver.Remote.assert_called_with("http://test:test@selenium.com", desired_capabilities)

    @patch('faf.driver.CONTEXT')
    def test_create_remote_appium_driver(self, mock_context):
        test_config = configparser.ConfigParser()
        test_config.add_section('remote_service')
        test_config.set('remote_service', 'remote_url', 'appium.com')
        test_config.set('remote_service', 'username', 'test')
        test_config.set('remote_service', 'access_key', 'test')
        test_config.add_section('application')
        test_config.set('application', 'name', 'test')
        mock_context.config = test_config
        args = Namespace(execution='appium_remote', capability='android6')
        desired_capabilities = {
            'appiumVersion': '1.8.1',
            'deviceName': 'Android Emulator',
            'deviceOrientation': 'portrait',
            'browserName': 'Chrome',
            'platformVersion': '6.0',
            'platformName': 'Android'
        }

        self.mock_appium_webdriver.Remote.return_value.session_id = '1234'
        with patch.object(faf.driver.Driver, '_Driver__name_saucelabs_job') as patched_set_saucelabs_name:
            faf.driver.Driver(args).get_driver()
            patched_set_saucelabs_name.assert_called_with('1234')

        self.mock_appium_webdriver.Remote.assert_called_with("http://test:test@appium.com", desired_capabilities)

    def test_raises_error_when_unrecognised_execution_argument(self):
        args = Namespace(execution='unknown')

        with pytest.raises(RuntimeError, match='Unable to set driver, unrecognised execution type: unknown'):
            faf.driver.Driver(args).get_driver()

    @patch('faf.driver.CONTEXT')
    def test_raises_error_when_remote_and_unknown_capability(self, mock_context):
        test_config = configparser.ConfigParser()
        test_config.add_section('remote_service')
        test_config.set('remote_service', 'remote_url', 'appium.com')
        test_config.set('remote_service', 'username', 'test')
        test_config.set('remote_service', 'access_key', 'test')
        mock_context.config = test_config
        args = Namespace(execution='selenium_remote', capability='unknown')

        with pytest.raises(KeyError, match='Remote capabilities config does not have section for selection: unknown'):
            faf.driver.Driver(args).get_driver()


