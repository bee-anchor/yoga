import os

from behave.__main__ import run_behave
from behave.configuration import Configuration
from faf.driver import set_driver
from faf.config import get_config
from faf.args import behave_parser

if __name__ == '__main__':

    args = behave_parser.parse_args()
    # config = get_config(args)
    set_driver(get_config())
    os.chdir(os.path.join(os.curdir, 'behave'))
    run_behave(Configuration())


