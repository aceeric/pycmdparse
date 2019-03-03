from multitype_enum import MultiTypeEnum
from opt_acceptresult_enum import OptAcceptResultEnum
from abstract_opt import AbstractOpt


class MultiParamOpt(AbstractOpt):
    """
    Implements a parameterized option taking at least one - and at most n - parameter
    values. E.g. "-f file1 file2' ('--file=file1 file2' functions identically
    because of how the command line is tokenized initially)

    Supports multiple parameter values as indicated by the 'multi_type' and 'count'
    fields. There are three multi option types, as indicated by the MultiTypeEnum enum.

    EXACTLY
    For this kind, as soon as the specified count of params is pulled from the cmd line
    stream, initialization completes. The param values are not inspected and so - can
    look like options. E.g., if count is 2 for a 'multi-files' option, and the
    command line is:

    "my-utility --multi-files foo --bar p1 p2"

    Then this would result in the multi-files option having parameters ['foo',
    '--bar'] and - assuming no other defined options - the positional params
    would be ['p1', 'p2']. Note that for this type - if the command line doesn't contain
    the required number of params, then it is a parse error.

    AT_MOST
    For this kind, the parser attempts to pull up to the specified count of parameters
    and the presence of an option terminates consumption of token from the command line.
    E.g.: if count is 4, and the command line is:

    "my-utility --multi-files foo --bar p1 p2"

    Then this would result in the multi-files option having parameters
    ['foo']. Then parsing would continue with --bar. If there's a --bar option
    defined then good, else it's a parse error.

    NO_LIMIT
    This pulls parameters from the command line until the next option is encountered
    (a token starting with dash) or the positional param option ("--") is encountered.
    If at the end of the command line stream, this can consume the positional params too.
    I.e., given this command line:

    "my-utility --multi-files foo bar p1 p2"

    The result would be the multi-files option having parameters ['foo', 'bar', 'p1', 'p2']
    and the positional parameters being empty. If the utility requires positional
    params, none would be available. To prevent that, the command line would need to
    look like:

    "my-utility --multi-files foo bar -- p1 p2"

    This class returns its value as a list which could be empty, but will never
    be 'None'.

    """
    def __init__(self, opt_name, short_key, long_key, opt_hint, required, is_internal, default_value,
                 multi_type, count, data_type, help_text):
        super().__init__(opt_name, short_key, long_key, opt_hint, required, is_internal, default_value,
                         data_type, help_text)
        self.multi_type = multi_type
        self._count = count
        self._value = []

    @property
    def value(self):
        return self._value

    def _do_accept(self, stack):
        if stack.size() < 2:
            return OptAcceptResultEnum.ERROR, "{}: requires a value, which was not supplied".format(self._supplied_key)
        self._supplied_key = stack.pop()
        while stack.size() > 0:
            if stack.peek().startswith("-") and self.multi_type != MultiTypeEnum.EXACTLY:
                # dash indicates an option: Terminates a multi-param option unless it's an exact count multi
                break
            if self.multi_type in [MultiTypeEnum.AT_MOST, MultiTypeEnum.EXACTLY] and len(self._value) == self._count:
                break
            self._value.append(stack.pop())

        if self.multi_type is MultiTypeEnum.EXACTLY and len(self._value) != self._count:
            return OptAcceptResultEnum.ERROR, "{}: expected {} parameters but only found {}".format(
                self._supplied_key, self._count, len(self._value))

        if self.data_type is not None:
            for i in range(0, len(self._value)):
                tmp = self._validate_datatype(self._value[i])
                if tmp is None:
                    return OptAcceptResultEnum.ERROR, "{}: {} has incorrect data type. Expected {}".format(
                        self._supplied_key, self._value[i], self.data_type.tostr())
                self._value[i] = tmp
        self._initialized = True
        return OptAcceptResultEnum.ACCEPTED,
