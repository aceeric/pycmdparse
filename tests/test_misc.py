from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum


def setup_function(function):
    CmdLine.reset()


def test_concatenated_bools():
    class TestCmdLine(CmdLine):
        """
        Tests that -a -b -c=foo is expressible as -abc=foo on the command line
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : bool
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : bool
                - name    : c_opt
                  short   : c
                  long    : c-opt
                  opt     : param
            '''
        a_opt = None
        b_opt = None
        c_opt = None

    args = "-abc=foo"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, so True
    assert TestCmdLine.a_opt
    # specified on the command line, so True
    assert TestCmdLine.b_opt
    # specified on the command line, so has the value from the command line
    assert TestCmdLine.c_opt == "foo"


def test_multi_param_opt_defaulted():
    class TestCmdLine(CmdLine):
        """
        Tests that --foo=bar and --fro bozz are handled the same way
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name      : foo_opt
                  short     : f
                  long      : foo
                  opt       : param
                - name      : fro_opt
                  short     : r
                  long      : fro
                  opt       : param
            '''
        foo_opt = None
        fro_opt = None

    args = "--foo=bar --fro bozz"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, no limit, no subsequent options or positional params so gets everything
    assert TestCmdLine.foo_opt == "bar"
    # not specified on the command line, so gets the default
    assert TestCmdLine.fro_opt == "bozz"


def test_multiple_cats():
    class TestCmdLine(CmdLine):
        """
        Tests that categories don't introduce parsing issues
        """
        yaml_def = '''
            supported_options:
              - category: the first
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : bool
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : bool
              - category: the second
                options:
                - name    : c_opt
                  short   : c
                  long    : c-opt
                  opt     : bool
                - name    : d_opt
                  short   : d
                  long    : d-opt
                  opt     : bool
            '''
        a_opt = None
        b_opt = None
        c_opt = None
        d_opt = None

    args = "-a --b-opt -c --d-opt"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.a_opt
    assert TestCmdLine.b_opt
    assert TestCmdLine.c_opt
    assert TestCmdLine.d_opt
