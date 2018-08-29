from collections import namedtuple


Config = namedtuple("Config", ['driver', 'debug', 'browser'])

CONFIG = None

def set_config():
    return Config(debug=False, driver='selenium', browser='chrome')



