from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.abstract_opt import AbstractOpt
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.positional_params import PositionalParams


def setup_function(function):
    CmdLine.reset()


def test_param_opt_validator():
    class TestCmdLine(CmdLine):
        """
        Test validation of a param-type option - using a validator defined
        in the CmdLine subclass
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : param
            '''

        @classmethod
        def validator(cls, to_validate):
            if isinstance(to_validate, AbstractOpt):
                if to_validate.opt_name == "a_opt":
                    if to_validate.value == "REJECTED":
                        return OptAcceptResultEnum.ERROR, "Invalid value: REJECTED"
            return None,

        a_opt = None

    args = "util-name -a REJECTED"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert TestCmdLine.parse_errors[0] == "Invalid value: REJECTED"


def test_positional_param_validator():
    class TestCmdLine(CmdLine):
        """
        Test validation of positional params - using a validator defined
        in the CmdLine subclass
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
                  opt     : param
            '''

        @classmethod
        def validator(cls, to_validate):
            if isinstance(to_validate, PositionalParams):
                if len(to_validate.params) != 3:
                    return OptAcceptResultEnum.ERROR, "Requires exactly three positional params"
            return None,

        a_opt = None

    args = "util-name -a -- P1 P2 P3 P4"
    parse_result = TestCmdLine.parse(args)
    assert len(TestCmdLine.positional_params) == 4
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert TestCmdLine.parse_errors[0] == "Requires exactly three positional params"


