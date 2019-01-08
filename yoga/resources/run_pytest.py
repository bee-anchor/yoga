import pytest
import sys
from yoga.yoga import test_env_setup
from yoga.args import yoga_pytest_argparser, pytest_args

if __name__ == '__main__':
    args = test_env_setup(yoga_pytest_argparser)
    res = pytest.main(pytest_args(args))
    sys.exit(res)
