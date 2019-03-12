"""
Tests how the parser handles repeating options. This is disallowed for
boolean options, but allowed for param options as follows:

if an option is exact, then it can be repeated for the number of occurrences
specified in the yaml count entry. If EXACT 2, then the following is valid:

my-utility --exact2 ONE --exact2 TWO

And the result is that field 'exact2'  contains the value ['ONE', 'TWO']

If EXACT 2, then the following is a parse error:

my-utility --exact2 ONE --exact2 TWO THREE

If an option is at-most, the same rule applies. E.g., if AT MOST 2, then
the following is valid:

my-utility --at-most2 ONE --at-most2 TWO

But the following causes a parse error:

my-utility --at-most2 ONE --at-most2 TWO THREE

For no-limit options, these can repeat indefinitely:

my-utility --no-limit ONE --no-limit TWO THREE --no-limit FOUR FIVE SIX ...

No user would do this, of course. Well...
"""
from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum


# noinspection PyUnusedLocal
def setup_function(function):
    CmdLine.reset()


def test_exactly_three_opt_repeating():
    """Shows a pitfall of EXACTLY. The first option consumes exactly three params
    without being stopped by a subsequent option. Because EXACT means the parser will
    try to get as many tokens as possible from the arg stream to match the specified
    count. Then when the third --test-opt option is parsed, the exact option count
    is already exceeded, triggering the parse error"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: exactly
              count     : 3
        '''
        test_opt = None
    args = "util-name --test-opt A --test-opt B --test-opt C"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert not TestCmdLine.test_opt  # no injection because of the parse error
    assert TestCmdLine.parse_errors[0] == "Arg parse error at: ['C']"


def test_exactly_one_opt_repeating():
    """Tests exactly one (because both type and count are omitted, hence default to
    'exactly one'. In this case, -opt FIRST -opt SECOND is the same as -opt FIRST SECOND
    and in this case, FIRST is consumed, satisfying the option, and then the parser
    tries to parse SECOND, this it doesn't know anything about and so it is a parse error."""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
        '''
        test_opt = None
    args = "util-name --test-opt A --test-opt B --test-opt C"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert not TestCmdLine.test_opt  # no injection because of the parse error
    assert TestCmdLine.parse_errors[0] == "Unsupported option: 'B'"


def test_exactly_one_opt_not_repeating():
    """Same as the test above with a different (equivalent) comand line"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
        '''
        test_opt = None
    args = "util-name --test-opt A B C"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert not TestCmdLine.test_opt  # no injection because of the parse error
    assert TestCmdLine.parse_errors[0] == "Arg parse error at: ['B', 'C']"


def test_bool_opt_repeating():
    """bool options aren't allowed to repeat"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : bool
        '''
        test_opt = None
    args = "util-name --test-opt --test-opt"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert not TestCmdLine.test_opt  # no injection because of the parse error
    assert "--test-opt already specified" in TestCmdLine.parse_errors[0]


def test_at_most_3_opt_repeating():
    """at-most params are terminated by another option in the arg stream so they can't
    pull options off the arg stream and interpret them as params"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              count     : 3
        '''
        test_opt = None
    args = "util-name --test-opt A --test-opt B C --test-opt D"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert not TestCmdLine.test_opt  # no injection because of the parse error
    assert TestCmdLine.parse_errors[0] == "Arg parse error at: ['D']"
