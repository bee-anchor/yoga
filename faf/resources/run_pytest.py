import pytest
from faf.faf import test_env_setup
from faf.args import faf_pytest_argparser, pytest_args

if __name__ == '__main__':
    args = test_env_setup(faf_pytest_argparser)
    pytest.main(pytest_args(args))


