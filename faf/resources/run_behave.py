import os

from behave.__main__ import run_behave
from behave.configuration import Configuration
from faf.driver import Driver
from faf.config import Config
from faf.args import behave_parser, arg_validation

if __name__ == '__main__':

    args = behave_parser.parse_args()
    arg_validation(args)
    Config(args).setup()
    if args.execution != 'non-ui':
        Driver(args).set_driver()
    os.chdir(os.path.join(os.curdir, 'behave'))
    run_behave(Configuration())


