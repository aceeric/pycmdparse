from pycmdparse.datatype_enum import DataTypeEnum
from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.abstract_opt import AbstractOpt


class BoolOpt(AbstractOpt):
    """
    Implements a boolean option. A boolean option doesn't accept a parameter,
    and defaults to a value of False. The presence of the option in the command line
    flips the option value to True.

    Say "-v" is the option, for "verbose". If the user provided "-v true", the parser
    would consume the "-v" option, set the corresponding option value to True, then attempt to
    parse the "true" token from the command line.

    In this case, one of three things happens: 1) If there are additional options (tokens prefixed
    with dash or double dash) to the right of the "true" param, then the parse returns
    an error "unsupported option: true". 2) If there are no additional options to the right, then
    "true" and everything to the right is taken as a positional parameter and the enclosing
    utility has to determine whether this is valid, unless: 3) If the command line spec (in the yaml)
    didn't specify any positional parameters, then it would be a parse error: Unsupported option.
    """

    def __init__(self, opt_name, short_key, long_key, opt_hint, required, is_internal, help_text):
        super().__init__(opt_name, short_key, long_key, opt_hint, required, is_internal, False,
                         DataTypeEnum.BOOL, help_text)
        # super init sets the object value to False, and sets initialized to True

    @property
    def value(self):
        return False if self._value is None else self._value

    def _do_accept(self, stack):
        """
        The existence of the option on the command line indicates True. e.g. "--doit" or
        "--truncate", etc.

        :param stack: the command line stack
        :return: always returns OptAcceptResultEnum.ACCEPTED
        """

        self._supplied_key = stack.pop()
        self._value = True
        return OptAcceptResultEnum.ACCEPTED,
