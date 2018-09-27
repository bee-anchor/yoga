import nose2
import sys
from faf.faf import test_env_setup
from faf.args import faf_nose_argparser, nose_args

if __name__ == '__main__':

    args = test_env_setup(faf_nose_argparser)
    res = nose2.discover(argv=nose_args(args)).runTests()
    sys.exit(res)


