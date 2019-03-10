"""
Tests that parse and show usage doesn't crash if things aren't
defined in the yaml. Doesn't validate usage. Just want to make
sure the parser isn't real easy to crash.
"""
from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum


def setup_function(function):
    CmdLine.reset()


def test_usage_utilname():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        utility:
            name: X
        '''
    TestCmdLine.parse("util-name")
    TestCmdLine.show_usage()


def test_usage_summary():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        summary: X 
        '''
    TestCmdLine.parse("util-name")
    TestCmdLine.show_usage()


def test_usage_usage():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        usage: X 
        '''
    TestCmdLine.parse("util-name")
    TestCmdLine.show_usage()


def test_usage_positional():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        positional_params:
          params: X
          text: X 
        '''
    TestCmdLine.parse("util-name")
    TestCmdLine.show_usage()


def test_usage_supported_opts():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : a-opt
        '''
    TestCmdLine.parse("util-name")
    TestCmdLine.show_usage()


def test_usage_details():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        details: X
        '''
    TestCmdLine.parse("util-name")
    TestCmdLine.show_usage()


def test_usage_addendum():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        summary: X
        '''
    TestCmdLine.parse("util-name")
    TestCmdLine.show_usage()
