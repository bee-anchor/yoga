import behave
from faf.faf import test_env_setup
from faf.args import faf_behave_argparser


if __name__ == '__main__':

    test_env_setup(faf_behave_argparser)
    behave.__main__.main()


