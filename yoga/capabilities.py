import configparser
import os


class Capabilities:

    def __init__(self, args):
        self.args = args

    def get_formatted_remote_capabilities(self):
        return self.__format_caps(self.get_remote_capabilities())

    def get_formatted_local_capabilities(self):
        return self.__format_caps(self.get_local_capabilities())

    def get_local_capabilities(self):
        local_caps_filepath = self.args.local_capabilities_file
        caps = self.__read_caps_file(local_caps_filepath)
        if not caps.has_section(self.args.capability):
            raise KeyError(f'Local capabilities config does not have section for selection: {self.args.capability}')
        return dict(caps[self.args.capability])

    def get_remote_capabilities(self):
        remote_caps_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            'remote', 'capabilities.ini')
        caps = self.__read_caps_file(remote_caps_filepath)
        if not caps.has_section(self.args.capability):
            raise KeyError(f'Remote capabilities config does not have section for selection: {self.args.capability}')
        return dict(caps[self.args.capability])

    @staticmethod
    def __read_caps_file(file_path):
        caps = configparser.ConfigParser()
        caps.optionxform = str
        caps.read(file_path)
        return caps

    @staticmethod
    def __format_caps(caps_dict):
        return str(caps_dict).replace('{', '').replace('}', '').replace("'", '')
