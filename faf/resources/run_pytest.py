import pytest
from faf.driver import Driver
from faf.args import pytest_parser, arg_validation, pytest_args
from faf.config import Config

if __name__ == '__main__':

    args = pytest_parser.parse_args()
    arg_validation(args)
    Config(args).setup()
    if args.execution != 'non-ui':
        Driver(args).set_driver()
    pytest.main(pytest_args(args))


