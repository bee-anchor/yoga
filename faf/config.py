import os
import configparser


CONFIG = None


class Config(object):


    def __init__(self, args):
        self.config_file_path = args.config
        self.args = args
        self.config = None

    def setup(self):
        '''
        Reads and validates config from the file defined in args. Assigns config to global CONFIG var. DO NOT USE
        THIS METHOD OTHER THAN AT THE VERY BEGINNING OF THE TEST ENVIRONMENT CREATION.
        :return:
        '''
        self.__validate_config_path()
        self.config = configparser.ConfigParser(self.__filtered_environment_vars(),
                                                interpolation=configparser.ExtendedInterpolation())
        self.config.read(self.config_file_path)
        self.__validate_config()
        self.__set_env_config()
        self.__set_config()


    @staticmethod
    def __filtered_environment_vars():
        # sometimes env vars can contain '$' (especially python virtual env ones) remove these from those passed in as
        # default else the config parser will raise an exception. (No user set env vars should have a '$', but if they
        # do, be aware these will not be available for interpolation in config files)
        env_vars = os.environ
        for key, value in env_vars.items():
            if value.rfind('$') >= 0:
                env_vars.pop(key)
        return env_vars

    def __validate_config_path(self):
        if not os.path.exists(self.config_file_path):
            raise FileNotFoundError(f'Configuration file "{self.config_file_path}" not found, check the path provided')

    def __validate_config(self):
        if self.args.execution == 'selenium_remote':
            expected_keys = ['selenium_url', 'results_url', 'job_timeout', 'username', 'access_key']
            for key in expected_keys:
                if not self.config.has_option('remote_service', key):
                    raise KeyError(f'Missing config for execution type of selenium_remote: [remote_service] {key}')
        elif self.args.execution == 'appium_remote':
            if not self.config.has_option('remote_service', 'appium_url'):
                raise KeyError(f'Missing config for execution type of appium_remote: [remote_service] appium_url')

    def __set_env_config(self):
        if not self.config.has_section(f'environment.{self.args.environment}'):
            raise KeyError(
                f'Missing environment config for selected env of {self.args.environment}, section required: [environment.{self.args.environment}]')
        env_config = self.config.items(f'environment.{self.args.environment}')
        self.__remove_env_config()
        self.config.add_section('environment')
        for key, value in env_config:
            self.config.set('environment', key, value)

    def __remove_env_config(self):
        environment_sections = [x for x in self.config.sections() if x.startswith('environment.')]
        for section in environment_sections:
            self.config.remove_section(section)

    def __set_config(self):
        global CONFIG
        CONFIG = self.config



