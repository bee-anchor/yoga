import pytest
import pdb
from argparse import Namespace
from faf.config import Config
import tempfile


class TestConfig():

    def test_config_setup_with_valid_args_sets_the_global_config(self):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
b'''[remote_service]
selenium_url = ondemand.saucelabs.com:80/wd/hub
appium_url: eu1.appium.testobject.com/wd/hub
results_url = https://saucelabs.com/beta/tests
job_timeout = "00
username = username
access_key = accesskey

[slack]
webhook = https://hooks.slack.com/services/hookhookhook

[environment.local]
url = https://testsite.com

[environment.test]
url = https://testsite.com
''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local', browser='chrome')
            Config(args).setup()

            from faf.config import CONFIG
            assert 'remote_service' in CONFIG.sections()
            assert 'environment' in CONFIG.sections()

    def test_config_setup_raises_exception_on_invalid_config_file(self):
        path = 'not/exists/path'
        args = Namespace(config=path)

        with pytest.raises(FileNotFoundError,
                           match=f'Configuration file "{path}" not found, check the path provided'):
            Config(args).setup()

    def test_config_setup_raises_exception_for_missing_remote_config_section(self):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
b'''[environment.local]
url = https://testsite.com
''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_remote')

            with pytest.raises(KeyError,
                               match='Missing config for execution type of selenium_remote: \[remote_service\]'):
                Config(args).setup()

    def test_config_setup_raises_exception_for_missing_selenium_remote_config_option(self):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
b'''[remote_service]
selenium_url = ondemand.saucelabs.com:80/wd/hub
results_url = https://saucelabs.com/beta/tests
job_timeout = "00
access_key = accesskey
''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_remote')

            with pytest.raises(KeyError,
                               match='Missing config for execution type of selenium_remote: \[remote_service\] username'):
                Config(args).setup()

    def test_config_setup_raises_exception_for_missing_appium_remote_config_option(self):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
b'''[remote_service]
selenium_url = ondemand.saucelabs.com:80/wd/hub
results_url = https://saucelabs.com/beta/tests
job_timeout = "00
username = username
access_key = accesskey
''')
            config.flush()
            args = Namespace(config=config.name, execution='appium_remote')

            with pytest.raises(KeyError,
                               match='Missing config for execution type of appium_remote: \[remote_service\] appium_url'):
                Config(args).setup()


    def test_config_setup_raises_exception_for_missing_env_config_section(self):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
b'''[remote_service]
selenium_url = ondemand.saucelabs.com:80/wd/hub
appium_url: eu1.appium.testobject.com/wd/hub
results_url = https://saucelabs.com/beta/tests
job_timeout = "00
username = username
access_key = accesskey

[slack]
webhook = https://hooks.slack.com/services/hookhookhook

[environment.test]
url = https://testsite.com
''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local',
                             browser='chrome')

            with pytest.raises(KeyError,
                               match=f'Missing environment config for selected env of local, section required: \[environment.local\]'):
                Config(args).setup()

    def test_config_setup_adds_all_chosen_env_config_and_removes_others(self):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
b'''[remote_service]
selenium_url = ondemand.saucelabs.com:80/wd/hub
appium_url: eu1.appium.testobject.com/wd/hub
results_url = https://saucelabs.com/beta/tests
job_timeout = "00
username = username
access_key = accesskey

[slack]
webhook = https://hooks.slack.com/services/hookhookhook

[environment.local]
url = https://testsite.com

[environment.test]
url = https://testsite.com
''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local',
                             browser='chrome')
            Config(args).setup()

            from faf.config import CONFIG
            assert 'environment.local' not in CONFIG.sections()
            assert 'environment.test' not in CONFIG.sections()
            assert 'environment' in CONFIG.sections()
            assert CONFIG.has_option('environment', 'url')

