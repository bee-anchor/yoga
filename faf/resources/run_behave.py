import behave
import sys
from faf.faf import test_env_setup
from faf.args import faf_behave_argparser, behave_args


if __name__ == '__main__':

    args = test_env_setup(faf_behave_argparser)
    res = behave.__main__.main(behave_args(args))
    sys.exit(res)

