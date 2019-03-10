"""
Tests permutations associated with param options with and without defaults,
with and without explicit param definition, required and optional opts,
and with and without values on the command line. If an option is defined
as required, then defaults are ignored as specified in the yaml. If no count
value is provided in the yaml, the package sets the paRAM count to
a value of one (1).
"""
from pycmdparse.cmdline import CmdLine
from pycmdparse.cmdline_exception import CmdLineException
from pycmdparse.parseresult_enum import ParseResultEnum


def setup_function(function):
    CmdLine.reset()

# Exact 1 special tests. Exact 1 parms provide their values as scalars rather
# than lists.


def test_exactly_explicit_default_array_size_1():
    """Tests the the default can be passed as an array for an exact 1 as long as there is only
    one element in the default array"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default-value]
              multi_type: exactly
              count     : 1
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "default-value"


def test_exactly_explicit_default_array_size_2():
    """Tests that an attempt to set a default for an exact 1 with a >1 array is disallowed"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: exactly
              count     : 1
              required  : false
        '''
        test_opt = None
    args = "util-name"
    try:
        parse_result = TestCmdLine.parse(args)
    except CmdLineException as e:
        assert "Invalid defaults supplied" in e.args[0]


def test_exactly_explicit_no_count_default_array_size_1():
    """If no count is specified, then a value of 1 is assigned"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default-value]
              multi_type: exactly
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "default-value"


def test_exactly_explicit_no_count_default_array_size_3():
    """If no count is specified, then a value of 1 is assigned. So an
     attempt to set a default with a >1 array is disallowed"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2, default3]
              multi_type: exactly
              required  : false
        '''
        test_opt = None
    args = "util-name"
    try:
        parse_result = TestCmdLine.parse(args)
    except CmdLineException as e:
        assert "Invalid defaults supplied" in e.args[0]

# Explicitly define an exact count option


def test_exactly_explicit_default_no_args_required():
    """exact count, explicitly specified, default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              multi_type: exactly
              count     : 1
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_exactly_explicit_default_no_args_optional():
    """exact count, explicitly specified, default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              multi_type: exactly
              count     : 1
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "default-value"


def test_exactly_explicit_default_args_required():
    """exact count, explicitly specified, default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              multi_type: exactly
              count     : 1
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"


def test_exactly_explicit_default_args_optional():
    """exact count, explicitly specified, default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              multi_type: exactly
              count     : 1
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"


def test_exactly_explicit_no_default_no_args_required():
    """exact count, explicitly specified, no default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: exactly
              count     : 1
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_exactly_explicit_no_default_no_args_optional():
    """exact count, explicitly specified, no default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: exactly
              count     : 1
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt is None


def test_exactly_explicit_no_default_args_required():
    """exact count, explicitly specified, no default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: exactly
              count     : 1
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"


def test_exactly_explicit_no_default_args_optional():
    """exact count, explicitly specified, no default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: exactly
              count     : 1
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"


# Implicitly define an exact count option. If the 'exactly' specifier is
# omitted, then the option is treated as 'exactly 1'. Meaning the injected field is
# provided as a scalar rather than a list. It's more natural to get the value like
# MyCmdLine.file_name == "foo" than to have to do: MyCmdLine.file_name[0] == "foo"
# So if the developer knows the param only accepts one value, the choice is to
# specify 'multi_type: exactly' and 'count: 1' in the yaml, or, omit both of those
# and the end results are identical.


def test_exactly_implicit_default_no_args_required():
    """exact count, implicitly specified, default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_exactly_implicit_default_no_args_optional():
    """exact count, implicitly specified, default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "default-value"


def test_exactly_implicit_default_args_required():
    """exact count, implicitly specified, default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"


def test_exactly_implicit_default_args_optional():
    """exact count, implicitly specified, default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : default-value
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"


def test_exactly_implicit_no_default_no_args_required():
    """exact count, implicitly specified, no default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_exactly_implicit_no_default_no_args_optional():
    """exact count, implicitly specified, no default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt is None


def test_exactly_implicit_no_default_args_required():
    """exact count, implicitly specified, no default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"


def test_exactly_implicit_no_default_args_optional():
    """exact count, implicitly specified, no default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt=cmdline"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == "cmdline"

# at most, explicit with count. At most is always explicit. If the count
# is provided, it is used as provided. If not provided, it is defaulted
# to one


def test_at_most_default_no_args_required():
    """at most, default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              count     : 3
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_at_most_default_no_args_optional():
    """at most, default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              count     : 3
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["default1", "default2"]


def test_at_most_default_args_required():
    """at most, default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              count     : 3
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_at_most_default_args_optional():
    """at most, default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              count     : 3
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_at_most_no_default_no_args_required():
    """at most, no default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              count     : 3
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_at_most_no_default_no_args_optional():
    """at most, no default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              count     : 3
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == []


def test_at_most_no_default_args_required():
    """at most, no default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              count     : 3
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_at_most_no_default_args_optional():
    """at most, no default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              count     : 3
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]

# At most explicit without count (count defaults to one if not provided)


def test_at_most_default_no_count_no_args_required():
    """at most, no count, default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_at_most_default_no_count_no_args_optional():
    """at most, no count, default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              required  : false
        '''
        test_opt = None
    args = "util-name"
    try:
        parse_result = TestCmdLine.parse(args)
    except CmdLineException as e:
        assert "Invalid defaults supplied" in e.args[0]


def test_at_most_default_no_count_args_required():
    """at most, no count, default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert "Arg parse error at" in TestCmdLine.parse_errors[0]


def test_at_most_default_no_count_args_optional():
    """at most, no count, default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: at-most
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    try:
        parse_result = TestCmdLine.parse(args)
    except CmdLineException as e:
        assert "Invalid defaults supplied" in e.args[0]


def test_at_most_no_count_no_default_no_args_required():
    """at most, no count, no default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_at_most_no_count_no_default_no_args_optional():
    """at most, no count, no default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == []


def test_at_most_no_count_no_default_args_required():
    """at most, no count, no default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert "Arg parse error at" in TestCmdLine.parse_errors[0]


def test_at_most_no_count_no_default_args_optional():
    """at most, no count, no default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: at-most
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.PARSE_ERROR.value
    assert "Arg parse error at" in TestCmdLine.parse_errors[0]


# No limit no count (count is ignored for no limit - whether
# supplied or not - hence no limit)


def test_no_limit_default_no_count_no_args_required():
    """no limit, no count, default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_no_limit_default_no_count_no_args_optional():
    """no limit, no count, default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["default1", "default2"]


def test_no_limit_default_no_count_args_required():
    """no limit, no count, default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_no_limit_default_no_count_args_optional():
    """no limit, no count, default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_no_limit_no_count_no_default_no_args_required():
    """no limit, no count, no default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_no_limit_no_count_no_default_no_args_optional():
    """no limit, no count, no default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == []


def test_no_limit_no_count_no_default_args_required():
    """no limit, no count, no default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_no_limit_no_count_no_default_args_optional():
    """no limit, no count, no default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]
    
# No limit with count specified (still ignored for no limit)

def test_no_limit_default_count_no_args_required():
    """no limit, count, default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              count     : -1
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_no_limit_default_count_no_args_optional():
    """no limit, count, default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              count     : -1
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["default1", "default2"]


def test_no_limit_default_count_args_required():
    """no limit, count, default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              count     : -1
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_no_limit_default_count_args_optional():
    """no limit, count, default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              default   : [default1, default2]
              multi_type: no-limit
              count     : -1
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_no_limit_count_no_default_no_args_required():
    """no limit, count, no default provided, no cmdline args, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              count     : -1
              required  : true
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.MISSING_MANDATORY_ARG.value


def test_no_limit_count_no_default_no_args_optional():
    """no limit, count, no default provided, no cmdline args, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              count     : -1
              required  : false
        '''
        test_opt = None
    args = "util-name"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == []


def test_no_limit_count_no_default_args_required():
    """no limit, count, no default provided, cmdline args provided, required option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              count     : -1
              required  : true
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]


def test_no_limit_count_no_default_args_optional():
    """no limit, count, no default provided, cmdline args provided, optional option"""
    class TestCmdLine(CmdLine):
        yaml_def = '''
        supported_options:
          - category:
            options:
            - name      : test_opt
              long      : test-opt
              opt       : param
              multi_type: no-limit
              count     : -1
              required  : false
        '''
        test_opt = None
    args = "util-name --test-opt cmdline1 cmdline2"
    parse_result = TestCmdLine.parse(args)
    assert parse_result.value == ParseResultEnum.SUCCESS.value
    assert TestCmdLine.test_opt == ["cmdline1", "cmdline2"]
