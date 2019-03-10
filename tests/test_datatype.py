import datetime

from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum


# noinspection PyUnusedLocal
def setup_function(function):
    CmdLine.reset()


def test_param_opt_1():
    """
    Test param option type - one for each data type:
    - valid data types
    - supplied on the command line
    """
    class TestCmdLine(CmdLine):
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : param
                  datatype: int
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : param
                  datatype: date
                - name    : c_opt
                  short   : c
                  long    : c-opt
                  opt     : param
                  datatype: decimal
            '''
        a_opt = None
        b_opt = None
        c_opt = None

    args = "util-name -a 123 -b 2019-12-31 -c 456.78"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.a_opt == 123
    assert TestCmdLine.b_opt.strftime("%Y-%m-%d") == "2019-12-31"
    assert TestCmdLine.c_opt == 456.78


def test_param_opt_2():
    """
    Test param option type - one for each data type:
    - valid data types
    - not supplied on the command line (but has yaml-defined defaults)
    """
    class TestCmdLine(CmdLine):
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : param
                  datatype: int
                  default : '123'
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : param
                  datatype: date
                  default : 2019-12-31
                - name    : c_opt
                  short   : c
                  long    : c-opt
                  opt     : param
                  datatype: decimal
                  default : 456.78
            '''
        a_opt = None
        b_opt = None
        c_opt = None

    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.a_opt == 123
    assert TestCmdLine.b_opt.strftime("%Y-%m-%d") == "2019-12-31"
    assert TestCmdLine.c_opt == 456.78


def test_param_opt_invalid():
    """
    Test param option type - one for each data type:
    - invalid data types
    - supplied on the command line
    - should emanate a parse error for each
    """
    class TestCmdLine(CmdLine):
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : param
                  datatype: int
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : param
                  datatype: date
                - name    : c_opt
                  short   : c
                  long    : c-opt
                  opt     : param
                  datatype: decimal
            '''
        a_opt = None
        b_opt = None
        c_opt = None

    args = "util-name -a 123.34"  # expects int
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert "has incorrect data type" in TestCmdLine.parse_errors[0]

    CmdLine.reset()
    args = "util-name -b notadate"  # expects date
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert "has incorrect data type" in TestCmdLine.parse_errors[0]

    CmdLine.reset()
    args = "util-name -c 2019-12-31"  # expects decimal
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert "has incorrect data type" in TestCmdLine.parse_errors[0]


def test_multi_param_opt_1():
    """
    Test param option type - one for each data type:
    - valid data types
    - supplied on the command line
    """
    class TestCmdLine(CmdLine):
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
                  datatype  : int
                - name      : b_opt
                  short     : b
                  long      : b-opt
                  opt       : param
                  multi_type: exactly
                  count     : 2
                  datatype  : date
                - name      : c_opt
                  short     : c
                  long      : c-opt
                  opt       : param
                  multi_type: exactly
                  count     : 2
                  datatype  : decimal
            '''
        a_opt = None
        b_opt = None
        c_opt = None

    args = "util-name -a 123 456 -b 2019-12-31 01-01-2019 -c 456.78 901.23"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.a_opt == [123, 456]
    assert TestCmdLine.b_opt == [datetime.datetime.strptime("2019-12-31", "%Y-%m-%d").date(),
                                 datetime.datetime.strptime("2019-01-01", "%Y-%m-%d").date()]
    assert TestCmdLine.c_opt == [456.78, 901.23]


def test_multi_param_opt_2():
    """
    Test param option type - one for each data type:
    - valid data types
    - not supplied on the command line (but has yaml-defined defaults)
    """
    class TestCmdLine(CmdLine):
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
                  datatype  : int
                  default   : [888, 777]
                - name      : b_opt
                  short     : b
                  long      : b-opt
                  opt       : param
                  multi_type: exactly
                  count     : 2
                  datatype  : date
                  default   : [2019-12-31, 04-05-2016]
                - name      : c_opt
                  short     : c
                  long      : c-opt
                  opt       : param
                  multi_type: exactly
                  count     : 2
                  datatype  : decimal
                  default   : [111.222, 333.444]
            '''
        a_opt = None
        b_opt = None
        c_opt = None

    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.a_opt == [888, 777]
    assert TestCmdLine.b_opt == [datetime.datetime.strptime("2019-12-31", "%Y-%m-%d").date(),
                                 datetime.datetime.strptime("2016-04-05", "%Y-%m-%d").date()]
    assert TestCmdLine.c_opt == [111.222, 333.444]


def test_multi_param_opt_invalid():
    """
    Test param option type - one for each data type:
    - invalid data types
    - supplied on the command line
    - should emanate a parse error for each
    """
    pass


def test_multi_param_opt():
    class TestCmdLine(CmdLine):
        """
        Test basic multi param: one equals, one at-most, and one no-limit with
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
    on the command line is a positional param
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
    assert TestCmdLine.positional_params == ["-NO", "--OPTIONS", "SO", "--", "ALL", "POSITIONAL"]
