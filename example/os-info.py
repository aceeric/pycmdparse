import sys

from pycmdparse.abstract_opt import AbstractOpt
from pycmdparse.cmdline import CmdLine
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.positional_params import PositionalParams


class MyCmdLine(CmdLine):
    """
    A simple utility that displays OS and Python info.
    """
    yaml_def = '''
    utility:
      name: os-info

    summary: >
      Gets operating system info, and saves it to
      the specified file.

    positional_params:
      params: FILE
      text: >
        Writes the information to FILE.

    supported_options:
      - category:
        options:
        - name : verbose
          short: v
          long : verbose
          opt  : bool
          help: >
            Provides additional (more verbose) information

    examples:
      - example: os-info -v my-outfile
        explanation: >
          Gets verbose operating system info and writes
          it to 'my-outfile' in the current working directory
    '''

    # Fields will be injected if not defined. If defined, their
    # values will be set by the parser. The 'name' key in the
    # yaml above specifies the Python field name to inject into
    # the subclass for each option your utility supports

    verbose = None


if __name__ == "__main__":
    parse_result = MyCmdLine.parse(sys.argv)
    if parse_result.value != ParseResultEnum.SUCCESS.value:
        MyCmdLine.display_info(parse_result)
        exit(1)
    import platform
    with open(MyCmdLine.positional_params[0], "w") as f:
        f.write("sys info: %s\n" % str(platform.uname()))
        if MyCmdLine.verbose:
            f.write("python version: %s\n" % platform.python_version())
