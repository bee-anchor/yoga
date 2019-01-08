import nose2
import sys
from yoga.yoga import test_env_setup
from yoga.args import yoga_nose_argparser, nose_args

if __name__ == '__main__':

    args = test_env_setup(yoga_nose_argparser)
    res = nose2.discover(argv=nose_args(args)).runTests()
    sys.exit(res)


