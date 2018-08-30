import os

from behave.__main__ import run_behave
from behave.configuration import Configuration
from faf.driver import set_driver
from faf.config import setup_config
from faf.args import behave_parser, arg_validation

if __name__ == '__main__':

    args = behave_parser.parse_args()
    arg_validation(args)
    setup_config(args)
    if args.execution != 'non-ui':
        set_driver(args)
    os.chdir(os.path.join(os.curdir, 'behave'))
    run_behave(Configuration())


