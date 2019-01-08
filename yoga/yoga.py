from yoga.context import CONTEXT
from yoga.config import Config
from yoga.driver import Driver
from yoga.args import arg_validation


def test_env_setup(arg_parser):
    '''
    Set up the environments for the tests to run in, sets context values and starts the driver (if relevant)
    :param arg_parser: the commandline arg parser to use for the test library that will be used
    :return: args: the command line args provided
    '''
    args = arg_parser.parse_args()
    CONTEXT.update_args(args)
    arg_validation(args)
    Config(args).setup()
    if args.execution != 'non-ui':
        Driver(args).set_driver()
    return args
