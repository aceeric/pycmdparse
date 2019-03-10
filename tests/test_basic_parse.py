from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum


def setup_function(function):
    CmdLine.reset()


def test_bool_opt():
    class TestCmdLine(CmdLine):
        """
        Test the bool option type - one provided on the command line, and one not
        A bool option type is False if not provided on the command line, else True
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : verbose
                  short   : v
                  long    : verbose
                  opt     : bool
                - name    : not_provided
                  short   : n
                  long    : not-provided
                  opt     : bool
            '''
        verbose = None
        not_provided = None

    args = "util-name --verbose"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, so True
    assert TestCmdLine.verbose
    # not specified on the command line, so False
    assert not TestCmdLine.not_provided


def test_param_opt():
    class TestCmdLine(CmdLine):
        """
        Test param option type - one provided on the command line and one not
        A param option is an option that takes exactly one param
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : param
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : param
            '''
        a_opt = None
        b_opt = None

    args = "util-name --b-opt=PASS"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # not specified on the command line, so None
    assert TestCmdLine.a_opt is None
    # specified on the command line, so has a value
    assert TestCmdLine.b_opt == "PASS"


def test_multi_param_opt():
    class TestCmdLine(CmdLine):
        """
        Test param: one equals, one at-most, and one no-limit with
        args provided so each param gets a defined number of values
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name      : a_opt
                  short     : a
                  long      : a-opt
                  opt       : param
                  multi_type: exactly
                  count     : 2
                - name      : b_opt
                  short     : b
                  long      : b-opt
                  opt       : param
                  multi_type: at-most
                  count     : 4
                - name      : c_opt
                  short     : c
                  long      : c-opt
                  opt       : param
                  multi_type: no-limit
                - name      : d_opt
                  short     : d
                  long      : d-opt
                  opt       : param
                  multi_type: no-limit
            '''
        a_opt = None
        b_opt = None
        c_opt = None
        d_opt = None

    args = "util-name --a-opt A1 A2 -b B1 B2 --c-opt C1 C2 C3"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, exactly 2
    assert TestCmdLine.a_opt == ["A1", "A2"]
    # specified on the command line, at most 4 but terminated by --c-opt
    assert TestCmdLine.b_opt == ["B1", "B2"]
    # specified on the command line, no limit so pulls all remaining tokens because no positional params
    assert TestCmdLine.c_opt == ["C1", "C2", "C3"]
    # not specified on the command line, so empty list
    assert TestCmdLine.d_opt == []


def test_positional_params():
    """
    No options specified - only positional params so everything
    on the command line is a positional param. Positional params are
    those tokens on the command line after all known options are parsed,
    or, all the tokens if there aren't any known options
    :return:
    """
    class TestCmdLine(CmdLine):
        yaml_def = '''
            positional_params:
              params:
              text:
            '''
        a_opt = None
        b_opt = None

    args = "util-name -NO --OPTIONS SO -- ALL POSITIONAL"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.positional_params.params == ["-NO", "--OPTIONS", "SO", "--", "ALL", "POSITIONAL"]
