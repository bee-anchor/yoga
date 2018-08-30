import pytest
from faf.driver import set_driver
from faf.args import pytest_parser, arg_validation, pytest_args
from faf.config import Config

if __name__ == '__main__':

    args = pytest_parser.parse_args()
    arg_validation(args)
    Config(args).setup()
    if args.execution != 'non-ui':
        set_driver(args)
    pytest.main(pytest_args(args))


