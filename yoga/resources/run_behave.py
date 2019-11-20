import behave
import sys
from yoga.yoga import test_env_setup
from yoga.args import yoga_behave_argparser, behave_args

if __name__ == '__main__':
    args = test_env_setup(yoga_behave_argparser)
    res = behave.__main__.main(behave_args(args))
    sys.exit(res)
