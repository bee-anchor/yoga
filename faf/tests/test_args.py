import pytest
from argparse import Namespace
from faf.args import nose_args, pytest_args, arg_validation


def test_arg_validation_fails_for_selenium_local_and_no_browser():
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_local, a browser must be specified'):
        args = Namespace(execution='selenium_local', browser=None)
        arg_validation(args)


def test_arg_validation_fails_for_selenium_remote_and_no_capabilities():
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_remote, appium_local or appium_remote, capability must be specified'):
        args = Namespace(execution='selenium_remote', capability=None)
        arg_validation(args)


def test_arg_validation_fails_for_appium_local_and_no_capabilities():
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_remote, appium_local or appium_remote, capability must be specified'):
        args = Namespace(execution='appium_local', capability=None)
        arg_validation(args)


def test_arg_validation_fails_for_appium_remote_and_no_capabilities():
    with pytest.raises(RuntimeError,
                       match='When using an execution type of selenium_remote, appium_local or appium_remote, capability must be specified'):
        args = Namespace(execution='appium_remote', capability=None)
        arg_validation(args)


def test_pytest_args_generates_maximum_possible_args():
    args = Namespace(test_dir='test/dir', keyword_expression='keyword', mark_expression='mark and mark1', debug=True)
    gen_args = pytest_args(args)
    assert gen_args == ['test/dir', '-k', 'keyword', '-m', 'mark and mark1', '--pdb']


def test_pytest_args_generates_minimum_possible_args():
    args = Namespace(test_dir=None, keyword_expression=None, mark_expression=None, debug=False)
    gen_args = pytest_args(args)
    assert gen_args == ['tests/']
