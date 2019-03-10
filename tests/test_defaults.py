from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum


def setup_function(function):
    CmdLine.reset()


def test_bool_param_defaulted():
    class TestCmdLine(CmdLine):
        """
        Test param option type with defaults - one provided and one not
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : param
                  default : a-default-value
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : param
                  default : b-default-value
            '''
        a_opt = None
        b_opt = None

    args = "util-name --a-opt a-on-the-command-line"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, so has the value from the command line
    assert TestCmdLine.a_opt == "a-on-the-command-line"
    # not specified on the command line, so gets the default value (always as a list)
    assert TestCmdLine.b_opt == "b-default-value"


def test_multi_param_opt_defaulted():
    class TestCmdLine(CmdLine):
        """
        Test param option type with defaults - one provided and one not
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name      : a_opt
                  short     : a
                  long      : a-opt
                  opt       : param
                  multi_type: no-limit
                - name      : b_opt
                  short     : b
                  long      : b-opt
                  opt       : param
                  multi_type: no-limit
                  default   : ["b-default-1", "b-default-2"]
                - name      : c_opt
                  short     : c
                  long      : c-opt
                  opt       : param
                  multi_type: no-limit
                  # here the default is not provided as a list but the ParamOpt
                  # will convert it to a list when it stores the default
                  default   : "c-default-1"
                - name      : d_opt
                  short     : d
                  long      : d-opt
                  opt       : param
                  multi_type: no-limit
                  # shows another way the default can be specified in the yaml
                  default:
                  - D1
                  - D2
                  - D3
            '''
        a_opt = None
        b_opt = None
        c_opt = None
        d_opt = None

    args = "util-name --a-opt A1 A2 A3"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, no limit, no subsequent options or positional params so gets everything
    assert TestCmdLine.a_opt == ["A1", "A2", "A3"]
    # not specified on the command line, so gets the default
    assert TestCmdLine.b_opt == ["b-default-1", "b-default-2"]
    # not specified on the command line, so gets the default (as a list, even though not a list in the yaml)
    assert TestCmdLine.c_opt == ["c-default-1"]
    # a default specified differently in the yaml
    assert TestCmdLine.d_opt == ["D1", "D2", "D3"]


def test_multi_param_opt_defaulted_and_cmdline():
    class TestCmdLine(CmdLine):
        """
        Tests a param option type with defaults - and values from the command line.
        The cmdline values should replace the defaults, not be appended
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name      : test_opt
                  short     : t
                  long      : test-opt
                  opt       : param
                  multi_type: no-limit
                  default   :
                  - DEFAULT1
                  - DEFAULT2
            '''
        test_opt = None

    args = "util-name --test-opt CMD1 CMD2 CMD3"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["CMD1", "CMD2", "CMD3"]  # not ["DEFAULT1", "DEFAULT2"]
