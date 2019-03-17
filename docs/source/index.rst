pycmdparse
==========
*pycmdparse* is a small library to help developers of Python console utilities parse the command line and display usage instructions. It's goal is to enable this with a minimum of programming. The Use Case for a console utility developer is:

1) Import this package and subclass the ``CmdLine`` class in your utility code
2) Initialize the ``yaml_def`` field (defined in the base class) with a yaml definition of options/params/usage
3) Call the ``parse`` function of the base class to parse the command line.

If successful, the ``parse`` function injects fields into your subclass - one for each option defined in the yaml spec. Your utility then accesses the injected fields to get the values provided by the user

If there is an error parsing the command line, or the user specifies -h or --help, your utility uses the base class ``display_info`` method to display the errors or display usage instructions - as specified in the yaml.

A simple example
^^^^^^^^^^^^^^^^
This is a console utility called "os-info":

.. code-block:: python

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
               f.write("python version: %s\n" %
                   platform.python_version())

If the user entered the following on the command line::

   os-info --help

They would see the following displayed on the console::

   os-info
   =======
   Gets the operating system version, and saves it to the
   specified file.

   Usage:

   os-info [-v,--verbose] FILE

   Writes the information to FILE.

   Options and parameters:

   -v,--verbose Optional. Provides additional (more verbose)
                information

   Examples:

   os-info -v my-outfile

   Gets verbose operating system info and writes it
   to 'my-outfile' in the current working directory

If the user entered the following on the command line::

   os-info --purple

They would see the following displayed on the console::

   Error:

   Unsupported option: '--purple'

   For usage instructions, try: os-info -h (or os-info --help)

Obviously with such a simple example, you wouldn't need ``pycmdparse``. The library is intended to help with complex command lines.

Terms
^^^^^

1) **arg**: An *arg* is a token on the command line. The first arg is the command name
2) **option**: An *option* is an argument used by the command. E.g.: --verbose
3) **parameter**: A *parameter* is a value that is used by an option or by the command. In this expression: ``--max-threads=100``, *--max-threads* is the option and *100* is the parameter. Positional parameters are parameters used by the command that are not paired with an option. In this expression: ``my-command FOO``, *FOO* is a positional param.

Features
^^^^^^^^

* Uses yaml to define command-line requirements and usage instructions
* Supports two types of option:

  * A **bool** option is true or false. Sometimes referred to as a switch. E.g.: -v, or --verbose. The value is false if omitted from the command line, and true if present on the command line
  * A **param** option takes one or more parameters. The default is a single param option. E.g.: --threads=100. But, a param option can be defined to accept an *exact* number of parameters, *up to* a specified number of parameters, or *no limit* to the number of parameters

* Supports short-form options (-v) and long-form options (--verbose). The yaml can specify both or either.
* Supports required and non-required options. Non-required options can have a default specified in the yaml. If a required option is omitted from the command line, then it is a parse error
* parameters can be expressed as follows on the command line: ``--max-threads=100``. ``--max-threads 100``. ``-t=100``. ``-t 100``. All are equivalent.
* Supports concatenation of short-form options. E.g.: ``-v -t -c`` and ``-vtc`` are handled identically. In addition, if a short-form option takes a value, it can also be concatenated. These are the same: ``-v -t -c=100`` and ``-vtc=100`` ``-vtc 100`` ``-v -t -c 100``
* Provides basic data typing of parameters: int, bool, float, date. If you specify a data type then the parser validates the parameter so you don't have to
* For options taking multiple params, these can be provided on the command line this way: ``--takes-three X Y Z`` or this way: ``--takes-three X --takes-three Y --takes-three Z``
* Supports the double dash ("--") option to indicate the beginning of positional parameters
* Parses positional parameters and provides them in a list
* Enables a custom validation call-back for you to perform any unique parameter validations
* Displays usage instructions in a generally consistent form - fitted to the width of the console window so you don't have to spend time on formatting help text in your utility
* Enables you to categorize your supported options. These categories are displayed in the usage instructions. So if you have groups or related sets of options, you can categorize them for readability,
* Enables you to explicitly define a brief usage scenario - like "my-utility [options] FILE". If you don't explicitly define a brief usage scenario, ``pycmdparse`` builds one for you from the defined supported options and positional params.
* Injects fields into your subclass based on the defined options so you have a simple way of accessing the command line values. Boolean options are python ``bool`` fields. Single-value param options are scalars. And multi-valued param options and positional params are lists.

The code
^^^^^^^^

https://github.com/aceeric/pycmdparse

Developer Guide
^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   devguide


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
