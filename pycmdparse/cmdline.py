import yaml

from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.opt_factory import  OptFactory
from pycmdparse.usage_example import UsageExample
from pycmdparse.cmdline_exception import CmdLineException
from pycmdparse.opt_category import OptCategory
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.positional_params import PositionalParams
from pycmdparse.showinfo import ShowInfo
from pycmdparse.splitter import Splitter


class CmdLine:
    """
    Provides the top-level functionality for the package. Usage:
    1) Import the package
    2) Sub-class this class
    3) Initialize the 'yaml_def' field in the subclass with a
       yaml definition of option/param/usage requirements
    4) Call the 'parse()' function to parse the command line. If successful,
       the function injects fields into the subclass - one for each option
       defined in the yaml spec.
    5) Access the fields injected into the subclass to get the values provided
       by the user on the command line
    6) If there is an error parsing the command line, use the class to display
       the errors, or, display usage instructions as specified in the yaml
    """

    yaml_def = None
    """A yaml string that defines the parsing requirements and usage instructions"""

    validator = None
    """
    A function that is called by the parser to perform customized validation of 
    positional params - and - individual options on the command line. The function
    must return a tuple: element zero is an OptAcceptResultEnum value, and
    element one is an error message to display to the user if element zero is 'ERROR'
    """

    program_name = None
    """The name of the program or utility that is importing the module"""

    summary = None
    """A very short summary that captures the key purpose of the utility"""

    usage = None
    """
    If None, then usage will be generated by the module from options and positional
    params. Otherwise specifies a abbreviated 'quick start' usage guidance
    """

    positional_params = None
    """
    After all options and option parameters are parsed, or, after '--' is encountered,
    everything else is a positional param. Stored in a PositionalParams object 
    """

    supported_options = None
    """
    A collection of supported options. The structure is a list of OptCategory objects,
    each of which contains a list of AbstractOpt-subclassed objects. Each AbstractOpt object defines
    the behavior of a command-line option/parameter. The parser uses the "name" field
    from each AbstractOpt object to inject a field - with that name - into the subclass of this
    class. The utility code can then reference the command line option value using
    this injected field.
    
    E.g., say an option was -'f' for 'file name'. Specifying 'filename' as the option name would 
    result in a field named 'filename' being added to the class. Say the user - when running
    the enclosing program - specified 'f=/my-file.tar' on the command line. After successful
    command-line parsing, the enclosing utility code would be able to rely on the existence
    of a field named 'filename' in this class having value '/my-file.tar'.
    """

    details = None
    """
    A section to provide additional, perhaps more technical, content below the usage and
    options sections
    """

    examples = None
    """
    A List of UsageExample objects, providing useful examples on how to run the enclosing
    program with common sets of options to solve common problems.
    """

    addendum = None
    """
    Free-form text after the examples. Used for copyright, licensing, bug report URLs.
    author information, Github URL, website URLs, etc.
    """

    parse_errors = None
    """Initialized by the parser with any errors encountered during command-line parsing"""

    @classmethod
    def reset(cls):
        """
        Supports testing. Nulls the class object out
        """
        cls.positional_params = None
        cls.supported_options = None
        cls.validator = None
        cls.details = None
        cls.addendum = None
        cls.examples = None
        cls.usage = None
        cls.summary = None
        cls.program_name = None
        cls.parse_errors = None
        cls.yaml_def = None

    @classmethod
    def __repr__(cls):
        val = ""
        for key, supported_option in cls.supported_options.items():
            val += str(supported_option) + ("\n" if len(val) == 0 else "")
        return val

    @classmethod
    def get_option(cls, option_name):
        """
        Gets an option using the name defined in the yaml path: category.options[n].name

        :param option_name: As specified in the option's "name" field in the yaml

        :return: the option object if one exists by the passed name, else None
        """
        flattened_options = CmdLine._flatten(cls.supported_options)
        for opt in flattened_options:
            if opt.opt_name == option_name:
                return opt
        return None

    @classmethod
    def display_info(cls, parse_result):
        """
        Shows usage, or shows errors, based on the passed result object. If the passed
        value indicates a parse error, then displays the errors in the internal
        class errors collection. If the passed value indicates to show usage instructions
        (e.g. if -h was provided on the command line) then shows the usage instructions
        defined in the yaml that was used to initialize the class.

        :param parse_result: the result of a prior command line parse operation
        """
        if parse_result in [ParseResultEnum.PARSE_ERROR, ParseResultEnum.MISSING_MANDATORY_ARG]:
            if cls.parse_errors is not None and len(cls.parse_errors) > 0:
                ShowInfo.show_errors(cls.parse_errors, cls.program_name)
        elif parse_result is ParseResultEnum.SHOW_USAGE:
            ShowInfo.show_usage(cls.program_name, cls.summary, cls.usage, cls.supported_options,
                                cls.details, cls.examples, cls.positional_params, cls.addendum)

    @classmethod
    def parse(cls, cmd_line):
        """
        Entry point for the class. Parses the yaml in the 'yaml_def' class field to initialize
        associated class fields, then parses the passed command line against the options defined
        by the yaml. If all is successful then adds one field to the class for each option, and
        initializes that field with the parameter specified on the command line for the
        option. (Or, for boolean options that don't take parameters, sets those values to True.)

        :param cmd_line: Can be a single string, which the function tokenizes and processes, or,
        can be a list, like the Python interpreter provides.

        :return: an ParseResultEnum, indicating the results of the command-line parse.
        """
        cls._init_from_yaml()
        has_options = True if cls.supported_options is not None else False
        if type(cmd_line) is str:
            cmdline_stack = Splitter.split_str(cmd_line, has_options)
        elif type(cmd_line) is list:
            cmdline_stack = Splitter.split_list(cmd_line, has_options)
        else:
            raise CmdLineException("Can only parse a string, or a list")
        return cls._parse(cmdline_stack)

    @classmethod
    def _parse(cls, cmdline_stack):
        """
        Actually does the command line parsing.

        :param cmdline_stack: as built from the command line. Left at top, right at
        bottom

        :return: a ParseResultEnum object indicating the result of the parse
        """
        flattened_options = CmdLine._flatten(cls.supported_options)
        if len(flattened_options) > 0:  # if empty, then no options, so all command-line args are positional params
            while cmdline_stack.size() > 0:
                if cmdline_stack.peek().lower() in ["-h", "--help"]:
                    return ParseResultEnum.SHOW_USAGE
                if cmdline_stack.peek() == "--":
                    cmdline_stack.pop()
                    cls._handle_positional_params(cmdline_stack)
                    break
                accept_result = OptAcceptResultEnum.IGNORED,
                for supported_option in flattened_options:
                    accept_result = supported_option.accept(cmdline_stack)
                    if accept_result[0] is not OptAcceptResultEnum.IGNORED:
                        break
                if accept_result[0] is OptAcceptResultEnum.IGNORED:
                    if not cmdline_stack.peek().startswith("-"):
                        if not cmdline_stack.has_options():
                            cls._handle_positional_params(cmdline_stack)
                        else:
                            cls._append_error("Unsupported option: '{0}'".format(cmdline_stack.peek()))
                            return ParseResultEnum.PARSE_ERROR
                    else:
                        cls._append_error("Unsupported option: '{0}'".format(cmdline_stack.peek()))
                        return ParseResultEnum.PARSE_ERROR
                elif accept_result[0] is OptAcceptResultEnum.ERROR:
                    cls._append_error(accept_result[1])
                    return ParseResultEnum.PARSE_ERROR

        if cmdline_stack.size() > 0:
            cls._handle_positional_params(cmdline_stack)

        if cmdline_stack.size() > 0:
            cls._append_error("Don't understand: {0}".format(cmdline_stack.pop_all()))
            return ParseResultEnum.PARSE_ERROR

        missing = [opt for opt in flattened_options if opt.required and not opt.initialized]

        if len(missing) != 0:
            cls._append_error("Mandatory option(s) not provided: {0}".format([opt.option_keys for opt in missing]))
            return ParseResultEnum.MISSING_MANDATORY_ARG

        if cls.validator is not None:
            for supported_option in flattened_options:
                accept_result = cls.validator(supported_option)
                if accept_result[0] is OptAcceptResultEnum.ERROR:
                    cls._append_error(accept_result[1])
                    return ParseResultEnum.PARSE_ERROR

            accept_result = cls.validator(cls.positional_params)
            if accept_result[0] is OptAcceptResultEnum.ERROR:
                cls._append_error(accept_result[1])
                return ParseResultEnum.PARSE_ERROR

        cls._add_fields()
        return ParseResultEnum.SUCCESS

    @staticmethod
    def _flatten(supported_opts):
        """
        Supported options are stored as lists, within categories. This reads all the
        option objects from the categories, and returns them as a single list, to avoid
        needing to constantly traverse the categories to get to the options.

        :param supported_opts: the class field that contains a list of categories,
        each of which contains a list of options

        :return: a list of only options
        """
        to_return = []
        if supported_opts is not None:
            for category in supported_opts:
                to_return.extend(category.options)
        return to_return

    @classmethod
    def _handle_positional_params(cls, cmdline_stack):
        """
        If the yaml defines positional parameters, then pops all the remaining
        tokens off the stack and stores them as positional parameters. Caller will
        have already made the determination that the remaining command line tokens are
        in fact positional parameters. (This function doesn't check.). If the yaml
        doesn't define positional parameters, then does nothing.

        :param cmdline_stack: the remaining tokens on the command line
        """
        if cls.positional_params is not None:
            cls.positional_params.params = cmdline_stack.pop_all()

    @classmethod
    def _append_error(cls, err_message):
        """
        Appends the passed error message to the class error list

        :param err_message: the error message to append
        """
        if cls.parse_errors is None:
            cls.parse_errors = []
        cls.parse_errors.append(err_message)

    @classmethod
    def _add_fields(cls):
        """
        For each supported option, adds a field to the class having the same name as
        the options's name in the supported options collection, and set the value of the
        class field to the value from the option object (i.e. the option's parameter.)
        The outer project code can then get the parameter directly from this class field
        rather than having to navigate the params collection, and then having to access
        the AbstractOpt subclass's interface.

        It's a little more intuitive way to access the option values. If the field is already
        present in the class, then this just sets the value, otherwise it creates the field
        and sets the value.
        """
        for opts in CmdLine._flatten(cls.supported_options):
            if not opts.opt_name.isidentifier():
                raise CmdLineException("Specified option name '{}' must be a valid Python identifier".format(
                    opts.opt_name))
            if opts.opt_name in dir(CmdLine):
                raise CmdLineException("Specified option name '{}' clashes".format(opts.opt_name))
            setattr(cls, opts.opt_name, opts.value)

    @classmethod
    def _init_from_yaml(cls):
        """
        Parses the yaml string in the class 'yaml_def' field, and initializes the following class
        fields from the yaml: program_name, summary, usage, positional_params, supported_options,
        details, examples, and addendum. If the yaml is missing an entry, then the corresponding
        class field is set to None.
        """
        parsed = yaml.load(cls.yaml_def, Loader=yaml.FullLoader)
        cls.program_name = parsed.get("program_name")
        cls.summary = parsed.get("summary")
        cls.usage = parsed.get("usage")
        if parsed.get("positional_params") is not None:
            cls.positional_params = PositionalParams(parsed.get("positional_params"))
        if parsed.get("supported_options") is not None:
            for category in parsed.get("supported_options"):
                opt_cat = OptCategory(category.get("category"))
                for opt in category.get("options"):
                    opt_cat.options.append(OptFactory.create_option(opt))
                if cls.supported_options is None:
                    cls.supported_options = []
                cls.supported_options.append(opt_cat)
        cls.details = parsed.get("details")
        if parsed.get("examples") is not None:
            for example in parsed.get("examples"):
                if cls.examples is None:
                    cls.examples = []
                cls.examples.append(UsageExample(example))
        cls.addendum = parsed.get("addendum")
