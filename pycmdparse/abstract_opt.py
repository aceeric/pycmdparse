import datetime
import re
from abc import ABC, abstractmethod
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.datatype_enum import DataTypeEnum


class AbstractOpt(ABC):
    """
    Provides the basic functionality to parse and store a value from the command line.
    Must be subclassed to provide specific functionality.
    """

    def __init__(self, opt_name, short_key, long_key, opt_hint, required, is_internal, default_value,
                 data_type, help_text):
        """
        Instance initializer for an option. Sets instance fields from passed values and performs
        some basic state initialization.

        :param opt_name: this is a valid Python identifier for the option. Once the parse
        process completes, this name will be used by the parser to inject a field - having
        this name - into the utility's CmdLine subclass, which can then be used to access
        the option value from the command line.
        :param short_key: E.g. "v", for "-v"
        :param long_key: E.g. "verbose", for "--verbose"
        :param opt_hint: For options accepting params, a mnemonic for the user that is
        presented in the usage instructions. E.g. if the usage instructions for the option
        looks like this: "-f,--filenane <pathspec>", then "pathspec" is the hint.
        :param required: True if the option must be supplied on the command line, else False
        :param is_internal: If True, then this is an internal option and doesn't appear on the
        usage instructions
        :param default_value: A default value. Ignored if this is a mandatory option. (It wouldn't
        make sense to require the user to provide an option on the command line but then
        specify a default value for that option.)
        :param data_type: Supports rudimentary data type validation. Expects a DataTypeEnum
        object
        :param help_text: Help text for the option
        """
        self._opt_name = opt_name
        self._short_key = short_key
        self._long_key = long_key
        self._opt_hint = opt_hint
        self._required = required
        self._is_internal = is_internal
        self._default_value = default_value
        self._data_type = data_type
        self._help_text = help_text
        if required and default_value is not None:
            self._initialized = True
            self._value = default_value
        else:
            self._initialized = False
            self._value = None
        self._supplied_key = None # they option actually encountered on the command line (e.g. "-f", or "--filename")

    def __repr__(self):
        s = "opt_name: {} short_key: {}; long_key: {}; value: {}; required: {}; hint: {}; is_internal: {}; "\
            "initialized: {}; default value: {}; data_type: {}; help_text: {}"
        return s.format(self.opt_name, self.short_key, self.long_key, self.value, self.required, self.opt_hint,
                        self.is_internal, self.initialized, self.default_value,
                        self.data_type, self.help_text)

    @property
    def opt_name(self):
        return self._opt_name

    @property
    def short_key(self):
        return self._short_key

    @property
    def long_key(self):
        return self._long_key

    @property
    def keys_and_hint(self):
        """
        Returns the keys and the hint for an option, formatted for help. The hint is a token
        or mnemonic that briefly lets the user know what parameter is expected for an option.

        :return: E.g.: if short key is "f" and long key is "file-name", and hint is is "pathspec",
        then returns: "-f, --file-name <pathspec>". If short key is "a" and long key is "action",
        and hint is is "upload|download", then returns: "-a, --action <upload|download>". If
        short key is "t" and long key is "timeout", and hint is is "n", then returns:
        "-t, --timeout <n>". Etc.
        """
        s = ""
        if self.short_key is not None:
            s += "-" + self.short_key
        if self.long_key is not None:
            s += "" if len(s) == 0 else ", "
            s += "--" + self.long_key
        if self.opt_hint is not None:
            s += " <" + self.opt_hint + ">"
        return s

    @property
    def initialized(self):
        """
        For boolean options this is always true because boolean options are initialized to
        have a value of False, and then the value is set to True if the option is specified on
        the command line. Therefore, boolean options are always initialized. Other options
        behave differently: A mandatory option is initialized if supplied on the command
        line. Otherwise it is not initialized. An non-mandatory option is initialized if
        a default was specified in the yaml, or, the option and parameter was provided
        on the command line.
        """
        return self._initialized

    @property
    def required(self):
        return self._required

    @property
    def opt_hint(self):
        return self._opt_hint

    @property
    def default_value(self):
        return self._default_value

    @property
    def data_type(self):
        return self._data_type

    @property
    def help_text(self):
        return self._help_text

    @property
    def is_internal(self):
        return self._is_internal

    @property
    def supplied_key(self):
        return self._supplied_key

    @property
    @abstractmethod
    def value(self):
        pass

    @property
    def option_keys(self):
        """
        Returns the keys formatted for usage help.

        :return: E.g. if short key is "-f" and long key is "--filename" then
        returns "-f,--filename". If only one or the other of short or long key
        is defined, then returns only that part.
        """
        to_return = ""
        if self.short_key is not None:
            to_return += "-" + self.short_key
        if self.long_key is not None:
            to_return += "/" if len(to_return) > 0 else ""
            to_return += "--" + self.long_key
        return to_return

    def accept(self, stack):
        """
        If the token on the top of the stack matches the short or long key for
        the option, then processes the token from the stack, delegating processing to a
        sub-class. If the option is successfully processed, then the stack is
        positioned at the next token so parsing can continue.

        :param stack: the command line stack

        :return: a tuple: element zero is an OptAcceptResultEnum value, element one is
        error message if element zero is OptAcceptResultEnum.ERROR
        """
        if stack.size() == 0:
            return OptAcceptResultEnum.IGNORED,
        if re.compile("-{1,2}\\w").match(stack.peek()) is None:
            # only match options starting with dash or double dash. (Triple-dash is ignored, according to
            # the philosophy of "prevent small problems")
            return OptAcceptResultEnum.IGNORED,
        if stack.peek().lstrip("-") in [self.short_key, self.long_key]:
            if self.supplied_key is not None:
                return OptAcceptResultEnum.ERROR, "Duplicate option specified on the command line: {}".format(stack.peek())
            return self._do_accept(stack)
        return OptAcceptResultEnum.IGNORED,

    def _validate_datatype(self, value):
        """
        The the option has a data type (which is not required) then validates that the option
        value matches the specified data type.

        :param value: the option value to validate

        :return: the passed value, converted to the object data type, if a data type is defined.
        If a data type is not defined, then returns None. If a data type is defined and the value
        doesn't match the type, then returns None.
        """
        if self.data_type is DataTypeEnum.INT:
            try:
                return int(value)
            except:
                return None
        elif self.data_type is DataTypeEnum.DECIMAL:
            try:
                return float(value)
            except:
                return None
        elif self.data_type is DataTypeEnum.DATE:
            try:
                return AbstractOpt._parse_date(value)
            except:
                return None
        return None

    @staticmethod
    def _parse_date(value):
        """
        Provides a really rudimentary date parser. Accepts YYYY-MM-DD and MM-DD-YYYY
        with separators of dash, period, or forward slash.

        :param value: a string to convert to a date

        :return: a datetime.datetime object if the conversion could be performed,
        otherwise None
        """
        formats = {
            "^[0-9]{2,4}([-/\\.])[0-9]{1,2}([-/\\.])[0-9]{1,2}$": "%Y1%m2%d",
            "^[0-9]{1,2}([-/\\.])[0-9]{1,2}([-/\\.])[0-9]{2,4}$": "%m1%d2%Y"
        }
        for format in formats.keys():
            p = re.compile(format)
            g = p.match(value)
            if g is not None and len(g.groups()) == 2:
                format = formats[format]
                format = format.replace("1", g.groups()[0]).replace("2", g.groups()[1])
                return datetime.datetime.strptime(value, format)
        return None

    @abstractmethod
    def _do_accept(self, stack):
        """
        Subclass-specific option handling

        :param stack: the command line stack. Subclass is expected to leave the stack ready for
        the next option to parse - meaning all tokens on the stack that belong to the option
        have been popped.

        :return: a tuple: element zero is an OptAcceptResultEnum value, element one is an
        error message if element zero is OptAcceptResultEnum.ERROR
        """
        pass

