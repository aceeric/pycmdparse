from pycmdparse.opt_acceptresult_enum import OptAcceptResultEnum
from pycmdparse.abstract_opt import AbstractOpt


class ParamOpt(AbstractOpt):
    """
    Implements a parameterized option taking only one parameter value. E.g.:
    '-f filename' or '--file=filename' or '--stuff="some stuff"', or
    '-s "some stuff"'
    """
    def __init__(self, opt_name, short_key, long_key, opt_hint, required, is_internal, default_value,
                 data_type, help_text):
        super().__init__(opt_name, short_key, long_key, opt_hint, required, is_internal, default_value,
                         data_type, help_text)

    @property
    def value(self):
        return self._value

    def _do_accept(self, stack):
        if stack.size() < 2:
            return OptAcceptResultEnum.ERROR, "{}: requires a value, which was not supplied".format(self._supplied_key)
        self._supplied_key = stack.pop()
        self._value = stack.pop()
        if self.data_type is not None:
            tmp = self._validate_datatype(self._value)
            if tmp is None:
                return OptAcceptResultEnum.ERROR, "{}: {} has incorrect data type. Expected {}".format(
                    self._supplied_key, self._value, self.data_type.tostr())
            self._value = tmp
        self._initialized = True
        return OptAcceptResultEnum.ACCEPTED,
