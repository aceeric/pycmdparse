from enum import Enum


class ParseResultEnum(Enum):
    """
    Defines the overall results of parsing the entire command line
    """

    SUCCESS = 1,
    """Command line parsed correctly"""
    PARSE_ERROR = 2,
    """Command line parsing failed"""
    SHOW_USAGE = 3
    """The -h, or the --help option was provided on the command line"""
    MISSING_MANDATORY_ARG = 4
    """A mandatory option was not provided on the command line"""

    @staticmethod
    def fromstr(enum_str):
        if enum_str is None:
            return None
        elif enum_str.lower() == "success":
            return ParseResultEnum.SUCCESS
        elif enum_str.lower() == "parse-error":
            return ParseResultEnum.PARSE_ERROR
        elif enum_str.lower() == "show-usage":
            return ParseResultEnum.SHOW_USAGE
        elif enum_str.lower() == "missing-mandatory":
            return ParseResultEnum.MISSING_MANDATORY_ARG
        else:
            return None

    def tostr(self):
        if self is ParseResultEnum.SUCCESS:
            return "success"
        elif self is ParseResultEnum.PARSE_ERROR:
            return "parse-error"
        elif self is ParseResultEnum.SHOW_USAGE:
            return "show-usage"
        elif self is ParseResultEnum.MISSING_MANDATORY_ARG:
            return "missing-mandatory"
