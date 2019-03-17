Developer Guide
===============

Getting Started
^^^^^^^^^^^^^^^
To use pycmdparse, you subclass the ``CmdLine`` class. The minimum requirement is to initialize the ``yaml_def`` base class field with a YAML string that defines the options and usage instructions for your utility. The intro section has an example of that. Here it is repeated.

This is an illustrative console utility called "os-info". This utility displays some information about the operating environment. This code would be in a python file in your utility:

.. code-block:: python

   import sys

   from pycmdparse.abstract_opt import AbstractOpt
   from pycmdparse.cmdline import CmdLine
   from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
   from pycmdparse.parseresult_enum import ParseResultEnum
   from pycmdparse.positional_params import PositionalParams

   class MyCmdLine(CmdLine):
       yaml_def = '''
       utility:
         name: os-info

       summary: >
         Gets operating system info, and saves it to
         the specified file.

       positional_params:
         params: FILE
         text: >
           Writes the information to FILE

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
               f.write("python version: %s\n" %
                   platform.python_version())

Key points:

1. The ``yaml_def`` base class field is initialized with yaml that defines the usage and options for the utilty
2. The main code calls the ``MyCmdLine.parse()`` method, passing ``sys.argv`` froim the Python interpreter. This initializes the base class from the yaml and then parses the command line in accordance with the yaml.
3. If the parse returns ``ParseResultEnum.SUCCESS`` then the code can access command line values using injected fields. In the example above, ``verbose`` is an injected field. (It's explicitly declared to avoid reference errors from the IDE.)
4. If the parse returns anything else, then the utility passes the return result to the base class ``display_info`` method to either display parse errors, or usage instructions.

YAML
^^^^
.. include:: yaml.rst

Option Examples
^^^^^^^^^^^^^^^
.. include:: optexample.rst

Custom Validation
^^^^^^^^^^^^^^^^^
.. include:: validator.rst
