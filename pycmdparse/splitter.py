import shlex

from cmdline_exception import CmdLineException
from stack import Stack


class Splitter:
    """
    Splits a command line into tokens.
    """

    @staticmethod
    def split_str(cmdline_str):
        """
        Splits a string, like "-f filename -ctv --foo=bar". First, the passed
        string is split with the shlex split function - which splits on all
        whitespace, preserving quoted substrings, and trims each resulting
        token. The resulting list is passed to the 'Splitter.split_list'
        function to handle breaking compound options, etc.

        :param cmdline_str: a string, such as one provided on a command line

        :return: a Stack. In the above example, would return a stack:
        '["-f", "filename", "-c", "-t", "-v", "--foo", "bar"]' with left
        at top and right at bottom. (First pop yields "-f".)
        """
        return Splitter.split_list(shlex.split(cmdline_str))

    @staticmethod
    def split_list(cmdline):
        """
        Splits a command line, like one provided by the Python interpreter.
        Splits concatenated single-char options into separate options. Splits
        "X=Y" into ["X", "Y"]

        The result is a list of tokens for subsequent left-to-right parsing.

        :param cmdline: a List. E.g.: '["-f", "filename", "-ctv", "--foo=bar"]'

        :return: a Stack. In the above example, would return a stack:
        '["-f", "filename", "-c", "-t", "-v", "--foo", "bar"]' with left
        at top and right at bottom. (First pop yields "-f".)
        """
        token_list = []
        in_positional_params = False
        for token in cmdline:
            if in_positional_params or token == "--":
                token_list.append(token)
                in_positional_params = True
            elif token[0] != '-':  # then it is a value
                token_list.append(token)
            elif token.startswith("--"):
                token_list.extend(Splitter._handle_long_form(token))
            else:
                token_list.extend(Splitter._handle_short_form(token))
        return Stack(token_list)

    @staticmethod
    def _handle_short_form(element):
        """
        Handles splitting apart a short form option

        E.g.: Given '-c', then generates ['-c']. Given '-cvf', then
        generates ['-c', '-v', '-f']. Given '-cvf=foo', then generates
        ['-c', '-v', '-f', 'foo']. Given '-cvf=', then generates ['-c', '-v',
        '-f', None]. (Not sure this latter feature is useful, but, since it
        could happen, it seems reasonable to handle it.)

        :param element: a short-form option: one that starts with single dash.
        Could be a concatenated short form option like '-cvf'. Can also be concatenated
        with the last option having a parameter, separated by the equals sign.

        :return: A list as described
        """
        if len(element) <= 1:
            raise CmdLineException("Invalid: " + element)
        tokens = []
        for i in range(1, len(element)):
            if element[i: i + 1] == "=":
                if i + 1 < len(element):
                    tokens.append(element[i + 1:])
                break
            tokens.append("-" + element[i: i + 1])
        return tokens

    @staticmethod
    def _handle_long_form(element):
        """
        Handles splitting apart a long form option

        E.g.: given '--foo=bar' then generates ['--foo', 'bar']. Given
        '--foo' then generates ['--foo']. Given '--foo=bar=baz', then generates
        ['--foo', 'bar=baz']. Given '--foo=', then generates ['--foo', None].
        (See '_handle_short_form'.)

        :param element:  a long-form option: one that starts with double dash.
        Could be stand-alone, like '--foo', or in the form '--foo=value'

        :return: A list as described
        """
        if len(element) <= 2:
            # then it can't possibly start with "--"
            raise CmdLineException("Invalid: " + element)
        tokens = element.split("=", 1)
        if len(tokens) == 2 and tokens[1].isspace():
            tokens[1] = None
        return tokens
