from enum import Enum
from .cmdline_exception import CmdLineException


class MultiTypeEnum(Enum):
    """
    Defines the type of a ParamOpt option
    """

    EXACTLY = 1,
    """The number supplied params must be exactly the specified value"""
    AT_MOST = 2,
    """The number supplied params can be one to the specified value"""
    NO_LIMIT = 3
    """The number supplied params can be zero or greater"""

    @staticmethod
    def fromstr(enum_str):
        if enum_str is None:
            return MultiTypeEnum.EXACTLY
        elif enum_str.lower() == "exactly":
            return MultiTypeEnum.EXACTLY
        elif enum_str.lower() == "at-most":
            return MultiTypeEnum.AT_MOST
        elif enum_str.lower() == "no-limit":
            return MultiTypeEnum.NO_LIMIT
        else:
            raise CmdLineException("Unknown param type: {}".format(enum_str))

    def tostr(self):
        if self is MultiTypeEnum.EXACTLY:
            return "exactly"
        elif self is MultiTypeEnum.AT_MOST:
            return "at-most"
        elif self is MultiTypeEnum.NO_LIMIT:
            return "no-limit"
