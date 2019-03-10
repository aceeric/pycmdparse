"""
Tests determination of the option name from the short form key, and long form
key as performed in the AbstractOpt class.

"""
from pycmdparse.cmdline import CmdLine
from pycmdparse.cmdline_exception import CmdLineException
from pycmdparse.parseresult_enum import ParseResultEnum


# noinspection PyUnusedLocal
def setup_function(function):
    CmdLine.reset()


def test_long_form_1():
    """Derive the option name from the long key that is already valid Python"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : testopt
              opt  : param
        '''
        testopt = None
    args = "util-name --testopt 123"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.testopt == '123'


def test_long_form_2():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : test-opt
              opt  : param
        '''
        test_opt = None
    args = "util-name --test-opt 123"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == '123'


def test_long_form_2a():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : test-opt
              opt  : param
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt is None


def test_long_form_3():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : test-opt
              opt  : bool
        '''
        test_opt = None
    args = "util-name --test-opt"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt


def test_long_form_4():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : test-opt
              opt  : bool
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert not TestCmdLine.test_opt


def test_short_form_1():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - short: t
              opt  : param
        '''
        t = None
    args = "util-name -t 123"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.t == '123'


def test_short_form_2():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - short: t
              opt  : param
        '''
        t = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.t is None


def test_short_form_3():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - short: t
              opt  : bool
        '''
        t = None
    args = "util-name -t"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.t


def test_short_form_4():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - short: t
              opt  : bool
        '''
        t = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert not TestCmdLine.t


def test_invalid_1():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            # no name -- no short or long key
            - opt  : bool
        '''
    args = "util-name"
    try:
        TestCmdLine.parse(args)
        assert False
    except CmdLineException as e:
        assert e.args[0] == "YAML must specify 'short' or 'long' option key"


def test_invalid_2():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : test/opt
              opt  : bool
        '''
    args = "util-name"
    try:
        TestCmdLine.parse(args)
        assert False
    except CmdLineException as e:
        assert e.args[0] == "Specified option name 'test/opt' must be a valid Python identifier"


def test_invalid_3():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - short: not-short
              opt  : bool
        '''
    args = "util-name"
    try:
        TestCmdLine.parse(args)
        assert False
    except CmdLineException as e:
        assert e.args[0] == "Invalid short key: 'not-short'"
