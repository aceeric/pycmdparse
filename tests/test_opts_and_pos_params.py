from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum


def setup_function(function):
    CmdLine.reset()


def test_options_and_positional_params_1():
    class TestCmdLine(CmdLine):
        """
        Tests that positional params are picked up when all known
        args are handled - everything remaining on the command line
        is a positional param
        """
        yaml_def = '''
            positional_params:
              params:
              text:
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
            '''
        a_opt = None
        b_opt = None

    args = "util-name -a THESE ARE POSITIONAL"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.a_opt
    assert not TestCmdLine.b_opt
    assert TestCmdLine.positional_params == ["THESE", "ARE", "POSITIONAL"]


def test_options_and_positional_params_2():
    class TestCmdLine(CmdLine):
        """
        Tests that the positional params option ("--") initiates positional
        params
        """
        yaml_def = '''
            positional_params:
              params:
              text:
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
            '''
        a_opt = None
        b_opt = None

    args = "util-name --b-opt -- THESE ARE POSITIONAL --a-opt"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert not TestCmdLine.a_opt
    assert TestCmdLine.b_opt
    assert TestCmdLine.positional_params == ["THESE", "ARE", "POSITIONAL", "--a-opt"]
