import argparse

base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument('-d', '--debug', action='store_true',
                         help='run in debug mode')
base_parser.add_argument('-c', '--config', default='config.ini', help="config file to use, defaults to 'config.ini'")
base_parser.add_argument('-o', '--override', nargs='+', help='config value override e.g. -o section.option=value section.option2=value2')
base_parser.add_argument('-e', '--environment', required=True, choices=['local', 'test'], help='environment to run in')
base_parser.add_argument('-x', '--execution', required=True,
                         choices=['selenium_local', 'selenium_remote', 'appium_local', 'appium_remote', 'grid_local', 'non-ui'],
                         help='execution type - type/location of driver')
base_parser.add_argument('-b', '--browser', choices=['chrome', 'firefox', 'internet explorer', 'safari', 'edge'],
                         help='browser to use for a local selenium execution')
base_parser.add_argument('-p', '--capability', help='which capability to use from relevant capabilities file (remote|local)')
base_parser.add_argument('-l', '--local-capabilities-file', default="local_capabilities.ini", help='path of local capabilities file (default is local_capabilties.ini)')
base_parser.add_argument('-s', '--slack_report', action='store_true', help='report test outcome to slack')

faf_nose_argparser = argparse.ArgumentParser(description='Run tests using nose', parents=[base_parser])
faf_nose_argparser.add_argument('--test-dir', help='directory containing tests to run')
faf_nose_argparser.add_argument('-n', '--test-names', nargs='+', help='names of tests to run')
faf_nose_argparser.add_argument('-a', '--attributes', nargs='+', help='filter which tests run using attributes')

faf_pytest_argparser = argparse.ArgumentParser(description='Run tests using pytest', parents=[base_parser])
faf_pytest_argparser.add_argument('--test-dir', help='directory containing tests to run')
faf_pytest_argparser.add_argument('-k', '--keyword-expression', help='only run tests which match the given substring expression (same as pytest -k)')
faf_pytest_argparser.add_argument('-m', '--mark-expression', help='only run tests matching given mark expression')

faf_behave_argparser = argparse.ArgumentParser(description='Run tests using behave', parents=[base_parser])
faf_behave_argparser.add_argument('--test_dir', required=True, help='directory containing behave tests and steps')
faf_behave_argparser.add_argument('-t', '--tags', help='tags filter for running tests')


def arg_validation(args):
    if args.execution != 'non-ui':
        if args.execution in {'selenium_local', 'grid_local'} and args.browser is None:
            raise RuntimeError('When using an execution type of selenium_local or grid_local, a browser must be specified (-b)')
        elif args.execution in {'selenium_remote', 'appium_local', 'appium_remote'} and args.capability is None:
            raise RuntimeError('When using an execution type of selenium_remote, appium_local or appium_remote, capability must be specified (-p)')


def nose_args(args):
    argv = []
    # add any specified named tests to run
    if args.test_names:
        argv.extend(args.test_names)
    argv.extend(['--plugin', 'nose2.plugins.attrib', '-s'])
    # add test directory location if specified, else the default location
    if args.test_dir:
        argv.append(args.test_dir)
    else:
        argv.append('tests/')
    if args.attributes:
        argv.extend(['-A', args.attributes])
    print(argv)
    return argv


def pytest_args(cmd_line_args):
    args = ['-s']
    # add test directory location if specified, else the default location
    if cmd_line_args.test_dir:
        args.append(cmd_line_args.test_dir)
    else:
        args.append('tests/')
    if cmd_line_args.keyword_expression:
        args.extend(['-k', cmd_line_args.keyword_expression])
    if cmd_line_args.mark_expression:
        args.extend(['-m', cmd_line_args.mark_expression])
    if cmd_line_args.debug:
        args.append('--pdb')
    return args


