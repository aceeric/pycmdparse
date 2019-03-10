import sys

from pycmdparse.abstract_opt import AbstractOpt
from pycmdparse.cmdline import CmdLine
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.positional_params import PositionalParams


class MyCmdLine(CmdLine):
    """
    Provides a template to clone into a new utility
    """

    yaml_def = '''
    utility:
      name:
      require_args: true # false

    summary: >
      TBD

    #usage: >
    # TBD

    positional_params:
      params: TBD
      text: >
        TBD

    supported_options:
      - category:
        options:
        - name    : tbd1
          short   : t
          long    : tbd-1
          hint    : tbd1
          required: false
          datatype:
          opt     :
          count   :
          default :
          help: >
            TBD
        - name    : tbd2
          short   : z
          long    : tbd-2
          hint    : tbd2
          required: false
          datatype:
          opt     :
          count   :
          default :
          help: >
            TBD

    details: >
      TBD

    examples:
      - example: TBD
        explanation: >
          TBD

      - example: TBD
        explanation: >
          TBD

    addendum: >
      TBD
    '''

    @classmethod
    def validator(cls, to_validate):
        some_error_condition = False
        if isinstance(to_validate, PositionalParams):
            if some_error_condition:
                return OptAcceptResultEnum.ERROR, "TODO error message"
        elif isinstance(to_validate, AbstractOpt):
            if to_validate.opt_name == "tbd1":
                if some_error_condition:
                    return OptAcceptResultEnum.ERROR, "TODO error message"
        return None,

    tbd1 = None
    tbd2 = None


if __name__ == "__main__":
    parse_result = MyCmdLine.parse(sys.argv)
    if parse_result.value != ParseResultEnum.SUCCESS.value:
        MyCmdLine.display_info(parse_result)
        exit(1)
    print("tbd1 = {}".format(MyCmdLine.tbd1))
    print("tbd2 = {}".format(MyCmdLine.tbd2))
    exit(0)
