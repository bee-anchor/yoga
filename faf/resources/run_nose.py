import nose2
from faf.driver import Driver
from faf.args import nose_parser, arg_validation, nose_argv
from faf.config import Config

if __name__ == '__main__':

    args = nose_parser.parse_args()
    arg_validation(args)
    Config(args).setup()
    if args.execution != 'non-ui':
        Driver(args).set_driver()
    nose2.discover(argv=nose_argv(args)).runTests()


