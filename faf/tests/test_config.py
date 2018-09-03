import pytest
from argparse import Namespace
from faf.config import Config
from faf.context import CONTEXT
import tempfile


class TestConfig():

    @pytest.fixture()
    def reset_context_config(self):
        CONTEXT.clear_config()
        yield

    def test_config_setup_with_valid_args_sets_the_global_config(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                remote_url = ondemand.saucelabs.com:80/wd/hub
                results_url = https://saucelabs.com/beta/tests
                job_timeout = 300
                username = username
                access_key = accesskey
                
                [slack]
                webhook = https://hooks.slack.com/services/hookhookhook
                
                [application]
                name = test
                
                [environment.local]
                url = https://testsite.com
                
                [environment.test]
                url = https://testsite.com
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local', browser='chrome',
                             override=None)
            Config(args).setup()

            assert 'remote_service' in CONTEXT.config.sections()
            assert 'environment' in CONTEXT.config.sections()

    def test_config_setup_raises_exception_on_invalid_config_file(self, reset_context_config):
        path = 'not/exists/path'
        args = Namespace(config=path)

        with pytest.raises(FileNotFoundError,
                           match=f'Configuration file "{path}" not found, check the path provided'):
            Config(args).setup()

    def test_config_setup_raises_exception_for_missing_application_config_section(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            args = Namespace(config=config.name)

            with pytest.raises(KeyError,
                               match="Missing 'application' section in the config"):
                Config(args).setup()

    def test_config_setup_raises_exception_for_missing_application_config_section(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[application]
                test = test
                ''')
            config.flush()
            args = Namespace(config=config.name)

            with pytest.raises(KeyError,
                               match="Missing 'name' option in the application section in the config"):
                Config(args).setup()

    def test_config_setup_raises_exception_for_missing_remote_config_section(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[application]
                name = test
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_remote')

            with pytest.raises(KeyError,
                               match='Missing config for execution type of selenium_remote/appium_remote: \[remote_service\]'):
                Config(args).setup()

    def test_config_setup_raises_exception_for_missing_selenium_remote_config_option(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                remote_url = ondemand.saucelabs.com:80/wd/hub
                results_url = https://saucelabs.com/beta/tests
                job_timeout = "00
                access_key = accesskey
                
                [application]
                name = test
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_remote')

            with pytest.raises(KeyError,
                               match='Missing config for execution type of selenium_remote/appium_remote: \[remote_service\] username'):
                Config(args).setup()

    def test_config_setup_raises_exception_for_missing_appium_remote_config_option(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                results_url = https://saucelabs.com/beta/tests
                job_timeout = "00
                username = username
                access_key = accesskey
                
                [application]
                name = test
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='appium_remote')

            with pytest.raises(KeyError,
                               match='Missing config for execution type of selenium_remote/appium_remote: \[remote_service\] remote_url'):
                Config(args).setup()


    def test_config_setup_raises_exception_for_missing_env_config_section(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                remote_url = ondemand.saucelabs.com:80/wd/hub
                results_url = https://saucelabs.com/beta/tests
                job_timeout = 300
                username = username
                access_key = accesskey
                
                [application]
                name = test
                
                [environment.test]
                url = https://testsite.com
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local',
                             browser='chrome')

            with pytest.raises(KeyError,
                               match=f'Missing environment config for selected env of local, section required: \[environment.local\]'):
                Config(args).setup()

    def test_config_setup_adds_all_chosen_env_config_and_removes_others(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                remote_url = ondemand.saucelabs.com:80/wd/hub
                results_url = https://saucelabs.com/beta/tests
                job_timeout = 300
                username = username
                access_key = accesskey
                
                [application]
                name = test
                
                [environment.local]
                url = https://testsite.com
                
                [environment.test]
                url = https://testsite.com
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local',
                             browser='chrome', override=None)
            Config(args).setup()

            assert 'environment.local' not in CONTEXT.config.sections()
            assert 'environment.test' not in CONTEXT.config.sections()
            assert 'environment' in CONTEXT.config.sections()
            assert CONTEXT.config.has_option('environment', 'url')

    def test_config_setup_overrides_config_when_override_args_provided(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                remote_url = ondemand.saucelabs.com:80/wd/hub
                results_url = https://saucelabs.com/beta/tests
                job_timeout = 300
                username = username
                access_key = accesskey
                
                [application]
                name = test
                
                [environment.local]
                url = https://testsite.com
                
                [environment.test]
                url = https://testsite.com
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local', browser='chrome',
                             override=['environment.url=https://new_url.com', 'remote_service.job_timeout=10'])
            Config(args).setup()

            assert CONTEXT.config['environment']['url'] == 'https://new_url.com'
            assert CONTEXT.config['remote_service']['job_timeout'] == '10'

    def test_config_setup_raises_error_when_override_section_not_present(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                remote_url = ondemand.saucelabs.com:80/wd/hub
                results_url = https://saucelabs.com/beta/tests
                job_timeout = 300
                username = username
                access_key = accesskey
                
                [application]
                name = test
                
                [environment.local]
                url = https://testsite.com
                
                [environment.test]
                url = https://testsite.com
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local', browser='chrome',
                             override=['nothere.test=test'])

            with pytest.raises(KeyError,
                               match=("Cannot override config using provided argument of 'nothere.test=test',"
                                      " there is no config section of 'nothere'")):
                Config(args).setup()

    def test_config_setup_raises_error_when_override_option_not_present(self, reset_context_config):
        with tempfile.NamedTemporaryFile() as config:
            config.write(
                b'''[remote_service]
                remote_url = ondemand.saucelabs.com:80/wd/hub
                results_url = https://saucelabs.com/beta/tests
                job_timeout = 300
                username = username
                access_key = accesskey
                
                [application]
                name = test
                
                [environment.local]
                url = https://testsite.com
                
                [environment.test]
                url = https://testsite.com
                ''')
            config.flush()
            args = Namespace(config=config.name, execution='selenium_local', environment='local', browser='chrome',
                             override=['environment.test=test'])

            with pytest.raises(KeyError,
                               match=("Cannot override config using provided argument of 'environment.test=test',"
                                      " there is no config option of 'test' in the 'environment' section")):
                Config(args).setup()

