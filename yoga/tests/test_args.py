import pytest
from argparse import Namespace
from yoga.args import pytest_args, arg_validation


def test_arg_validation_fails_for_selenium_local_and_no_browser():
    args = Namespace(execution='selenium_local', browser=None)
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_local or grid_local, a browser must be specified'):
        arg_validation(args)


def test_arg_validation_fails_for_grid_local_and_no_browser():
    args = Namespace(execution='grid_local', browser=None)
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_local or grid_local, a browser must be specified'):
        arg_validation(args)


def test_arg_validation_fails_for_selenium_remote_and_no_capabilities():
    args = Namespace(execution='selenium_remote', capability=None)
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_remote, appium_local, appium_remote '
                             'or appium_remote_real, capability must be specified'):
        arg_validation(args)


def test_arg_validation_fails_for_appium_local_and_no_capabilities():
    args = Namespace(execution='appium_local', capability=None)
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_remote, appium_local, '
                             'appium_remote or appium_remote_real, capability must be specified'):
        arg_validation(args)


def test_arg_validation_fails_for_appium_remote_and_no_capabilities():
    args = Namespace(execution='appium_remote', capability=None)
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_remote, appium_local, '
                             'appium_remote or appium_remote_real, capability must be specified'):
        arg_validation(args)


def test_arg_validation_fails_for_appium_remote_real_and_no_capabilities():
    args = Namespace(execution='appium_remote_real', capability=None)
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_remote, appium_local, '
                             'appium_remote or appium_remote_real, capability must be specified'):
        arg_validation(args)


def test_pytest_args_generates_maximum_possible_args():
    args = Namespace(test_dir='test/dir', keyword_expression='keyword', mark_expression='mark and mark1',
                     debug=True, reruns=False, additional_args='')
    gen_args = pytest_args(args)
    assert gen_args == ['-s', '--tb=short', 'test/dir', '-k', 'keyword', '-m', 'mark and mark1',
                        '--pdb', '--pdbcls=IPython.terminal.debugger:TerminalPdb']


def test_pytest_args_generates_minimum_possible_args():
    args = Namespace(test_dir=None, keyword_expression=None, mark_expression=None, debug=False,
                     reruns=False, additional_args='')
    gen_args = pytest_args(args)
    assert gen_args == ['-s', '--tb=short', None]
