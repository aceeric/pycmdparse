from pycmdparse.cmdline import CmdLine
from pycmdparse.parseresult_enum import ParseResultEnum
from pycmdparse.cmdline_exception import CmdLineException


# noinspection PyUnusedLocal
def setup_function(function):
    CmdLine.reset()


def test_concatenated_bools():
    class TestCmdLine(CmdLine):
        """
        Tests that -a -b -c=foo is expressible as -abc=foo on the command line
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : bool
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : bool
                - name    : c_opt
                  short   : c
                  long    : c-opt
                  opt     : param
            '''
        a_opt = None
        b_opt = None
        c_opt = None

    args = "util-name -abc=foo"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, so True
    assert TestCmdLine.a_opt
    # specified on the command line, so True
    assert TestCmdLine.b_opt
    # specified on the command line, so has the value from the command line
    assert TestCmdLine.c_opt == "foo"


def test_multi_param_opt_defaulted():
    class TestCmdLine(CmdLine):
        """
        Tests that --foo=bar and --fro bozz are handled the same way
        """
        yaml_def = '''
            supported_options:
              - category:
                options:
                - name      : foo_opt
                  short     : f
                  long      : foo
                  opt       : param
                - name      : fro_opt
                  short     : r
                  long      : fro
                  opt       : param
            '''
        foo_opt = None
        fro_opt = None

    args = "util-name --foo=bar --fro bozz"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    # specified on the command line, no limit, no subsequent options or
    # positional params so gets everything
    assert TestCmdLine.foo_opt == "bar"
    # not specified on the command line, so gets the default
    assert TestCmdLine.fro_opt == "bozz"


def test_multiple_cats():
    class TestCmdLine(CmdLine):
        """
        Tests that categories don't introduce parsing issues
        """
        yaml_def = '''
            supported_options:
              - category: the first
                options:
                - name    : a_opt
                  short   : a
                  long    : a-opt
                  opt     : bool
                - name    : b_opt
                  short   : b
                  long    : b-opt
                  opt     : bool
              - category: the second
                options:
                - name    : c_opt
                  short   : c
                  long    : c-opt
                  opt     : bool
                - name    : d_opt
                  short   : d
                  long    : d-opt
                  opt     : bool
            '''
        a_opt = None
        b_opt = None
        c_opt = None
        d_opt = None

    args = "util-name -a --b-opt -c --d-opt"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.a_opt
    assert TestCmdLine.b_opt
    assert TestCmdLine.c_opt
    assert TestCmdLine.d_opt


def test_empty_1():
    class TestCmdLine(CmdLine):
        pass
    args = "util-name -v"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value  # no yaml no parse
    assert TestCmdLine.parse_errors[0] == "Arg parse error at: ['-v']"
    TestCmdLine.display_info(parse_result)  # for coverage


def test_empty_2():
    class TestCmdLine(CmdLine):
        pass
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value  # no args so, success
    # nothing happens - just make sure it doesnt raise
    TestCmdLine.show_usage()


def test_no_args_arg_required():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        utility:
            name: X
            require_args: true
            '''

    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert TestCmdLine.parse_errors[0] == "At least one option or param is required"


def test_invalid_parse_object():
    """Parser can only handle strings and lists"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: exactly
              required  : false
        '''
        test_opt = None
    args = "util-name", "X", "Y", "Z"  # tuple
    try:
        TestCmdLine.parse(args)
    except CmdLineException as e:
        assert e.args[0] == "Can only parse a string or a list"


def test_single_dash():
    """'-' is an invalid cmd line option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: exactly
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt ZZZ -"
    try:
        TestCmdLine.parse(args)
    except CmdLineException as e:
        assert e.args[0] == "Invalid option: '-'"


def test_unknown_param_type():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: invalid
        '''
        test_opt = None
    args = "util-name"
    try:
        TestCmdLine.parse(args)
    except CmdLineException as e:
        assert e.args[0] == "Unknown param type: invalid"


def test_unknown_option_type():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : invalid
        '''
        test_opt = None
    args = "util-name"
    try:
        TestCmdLine.parse(args)
    except CmdLineException as e:
        assert e.args[0] == "Unknown option type: invalid"


def test_repr():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : test-opt
              opt  : bool
        '''
    args = "util-name --test-opt"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    test_opt = TestCmdLine.get_option("test_opt")  # for coverage
    repr(test_opt)  # for coverage
    test_opt = TestCmdLine.get_option("doesnt_exist")  # for coverage
    assert not test_opt


def test_name_clash():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : _supported_options
              opt  : bool
        '''
    _supported_options = None

    args = "util-name"
    try:
        TestCmdLine.parse(args)
    except CmdLineException as e:
        assert e.args[0] == "Specified option name '_supported_options' clashes"


def test_no_param():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - long : test
        '''
    _supported_options = None

    args = "util-name --test"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert TestCmdLine.parse_errors[0]\
           == "test: requires a value, which was not supplied"


def test_no_cat():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          options:
          - long : _supported_options
            opt  : bool
        '''
    _supported_options = None

    args = "util-name"
    try:
        TestCmdLine.parse(args)
    except CmdLineException as e:
        assert e.args[0].startswith("Error parsing the yaml")

def test_full_usage():
    class TestCmdLine(CmdLine):
        yaml_def = '''
        utility:
          name: xyz
          require_args: false
    
        summary: >
          Test
    
        #usage: >
        # TBD
    
        positional_params:
          params: N/A
          text: >
            Test
    
        supported_options:
          - category: foo
            options:
            - name      : a
              short     : a
              long      : aa
              hint      : a
              required  : false
              datatype  :
              opt       : param
              multi_type: no-limit
              count     : a
              default   :
              help: >
                Test
    
        details: >
          Test
    
        examples:
          - example: Test
            explanation: >
              Test
    
        addendum: >
          Test
        '''
    args = "xyz --help"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SHOW_USAGE.value
    TestCmdLine.display_info(parse_result)  # for coverage
