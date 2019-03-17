Here is an empty schema for ``pycmdparse``. The elipsis (...) indicate that a value is required. This shows the structure of the yaml. Below, each section is documented. Note - every top-level section in the yaml is optional.
::

    utility:
      name: ...
      require_args: ...
    summary: >
      ...
    usage: >
      ...
    positional_params:
      params: ...
      text: >
        ...
    supported_options:
      - category: ...
        options:
        - name      : ...
          short     : ...
          long      : ...
          hint      : ...
          opt       : ...
          required  : ...
          datatype  : ...
          multi_type: ...
          count     : ...
          help: >
            ...
    details: >
      ...
    examples:
      - example: ...
        explanation: >
          ...
    addendum: >
      ...

Here are the details on the schema. In this section, example content will be provided, replacing the elipsis above. The content will be for a hypothetical *foo-utility*.

**Utility**
::

    utility:
        name: foo-utility
        require_args: true

The *name* key identifies the utility name - what users will invoke on the command line. In this case, it is the *foo-utility*. In the usage instructions, this utility name displays at the top of the usage instructions, with a double underline.

If you want to require options and/or positional params, specify *require_args*: true. Then, if the user just offers the utility name on the command line with no args, the parser will return a parse result of SHOW_USAGE. If *require_args* is false in the yaml or omitted, then if the user simply types the utility name on the command line, this will not cause a parse error. This could be useful in a situation where your utility has defaults for every single command line option/param - or - doesn't support any command line options/params.

**Summary**
::

    summary: >
        The foo-utility searches the internet for all available
        information about the etymology of 'foo'. (See
        https://en.wikipedia.org/wiki/Foobar). Various options and
        parameters can be provided as command line arguments to tailor
        the behavior of the utility.

Provide a top-line summary to help the user quickly understand the purpose of the utility. This displays to the console under the program name in the help.

**Usage**
::

    usage: >
     foo-utility [options] PREVIOUSFOO

The *usage* section is a really brief synopsis of what the command line looks like to invoke the utility. If there is no usage section, then usage is generated to the console by pycmdparse from the defined options/parameters as well as the *positional_params*. (An example of pycmdparse-generated usage is shown in the positional params section below.)

This example provides an explicit usage section. So, whatever is provided here is displayed verbatim.

**Positional Params**
::

    positional_params:
      params: PREVIOUSFOO
      text: >
        PREVIOUSFOO is an optional file spec. If the results of a prior
        foo analysis are available in the PREVIOUSFOO file, then the
        utility only displays the deltas between the current foo
        etymology, and the etymology saved in the specified file.
        This parameter can be an absolute - or relative - file
        specifier.

The existence of the *positional_params* entry causes positional param parsing. Positional params are everything after "-\\-" on the command line, or, everything on the command line after all known options are parsed, or, everything on the command line if there are no defined options.

The *positional_params* entry contains two sub-entries: *params*, and *text*. Both are used only to format usage to the console - and only if the *usage* entry above is not provided. The value of the *params* key is appended to the supported options, and the *text* is appended to that, on a separate line. So the pycmdparse-generated usage - including supported options and positional params - for the foo-utility - would print to the console as follows, using the *positional_params* spec in this yaml::

     Usage:

     foo-utility [-v,--verbose] [-h,--help]
                 [-d,--depth <n>]
                 [-e,--exclude <term1 ...>] PREVIOUSFOO

     PREVIOUSFOO is an optional file spec. If the results of a prior foo
     analysis are available in the PREVIOUSFOO file, then the utility
     only displays the deltas between the current foo etymology, and the
     etymology saved in the specified file. This parameter can be an
     absolute - or relative - file specifier.

Note that the *params* entry has no meaning to pycmdparse. It's only a  mnemonic for the user.

**Supported Options**
::

    supported_options:
      - category: Common options
        options:
        - name    : verbose
          short   : v
          long    : verbose
          opt     : bool
          help: >
            Causes verbose output. Can result in significant volumes of
            information to be emanated to the console. Use with caution.
        - name    : help
          short   : h
          long    : help
          opt     : bool
          help: >
            Displays this help text.
      - category: Less common options
        options:
        - name      : depth
          short     : d
          long      : depth
          hint      : n
          required  : false
          datatype  : int
          opt       : param
          default   : 1
          help: >
            Specifies the recursion level of the search. If not
            specified on the command line, then a default value
            of one (1) is used. Increasing the recursion level
            can provide a better analysis result, but can
            significantly increase the processing time.
            The max value is 92.
        - name      : exclude
          short     : e
          long      : exclude
          hint      : term1 ...
          required  : false
          opt       : param
          multi_type: no-limit
          count     :
          help: >
            Specifies a list of terms that cause the utility
            to stop recursing at any given level. Multiple terms
            can be provided. There is no limit to the number
            of terms.

The *supported_options* entry defines the options and associated params for the utility. If this entry exists, then option parsing occurs. Otherwise, no option parsing occurs. All options support a single-character (short) form, and/or a long form. Example: ``-t``, and ``--timeout``. Options are case-sensitive. There are two types of options:

An example of a *bool* is: ``--verbose``. It is False by default, and only True if provided on the command line. It is always optional, since it always has a value.

A *param* option is an option taking one or more params, like ``--filelist FILE1 FILE2 FILE3``, or ``--file FILE``. A param option's parameters are terminated differently depending on the param type. More details are provided below.

Param options are either required, or not required. Required options that are not provided on the command line cause a parse error. Non-required options can have a default in the yaml. Non-required options that are not provided on the command line and that don't have default specified have a value of ``None`` upon conclusion of arg parsing.

All options must belong to a category. If the category entry has a value, then it is displayed to the console when usage instructions are displayed. Otherwise the presence of the category has no effect. The purpose is to support categorization of options, which some complex utilities will want. The fact that it is required in the yaml just simplifies the pycmdparse yaml handling. Multiple categories are supported but not required.

The example foo-utility supports the following options: ``--verbose``, ``--exclude``, and ``--depth``. ``--verbose`` is boolean, ``--exclude`` is param accepting multiple values, and ``--depth`` is param accepting only a single value.

Each option is an array of key/value entries. The supported keys are listed for each option type. If a key is omitted, its value is None.  Each option requires either a short-form _or_ long-form option key.  Both are allowed.

The table below describes the behavior of each of the keys used to define an option:

==========  =====================================================================
key         description
==========  =====================================================================
name        Optional. The Python field name that you want injected into
            your subclass to hold the option value. Must be a valid Python
            identifier. If not supplied, then ``pycmdparse`` will use either
            the long key, or the short key for the field to inject. If the
            long key is used, dashes in the long key are replaced by underscores
            to try to make a valid identifier. If an invalid identifier is
            defined explicitly or through derivation from the long or short
            key, an exception is thrown.
short       The short (single-character) option. E.g. "v" will match ``-v`` on the
            command line. Don't include the dash in the yaml.
long        The long option. E.g. "verbose" will match ``--verbose`` on the command
            line. Either a short - or a long - option is required. Both can be
            provided. Don't include the double-dash in the yaml.
opt         The option type. Either *bool*, or *param*. If omitted, then the option is
            defined as a *param* option taking exactly one value. E.g.:
            ``--max-threads=1``
hint        An optional mnemonic to the user for param-type options. E.g., if you have
            an option ``--timeout-interval``, you might define a hint of "n" to let the
            user know via the usage instructions that a number is expected. If you
            do this in the yaml, then in the usage instructions, the option displays
            like this: ``-t, --timeout-interval <n>``
required    true or false indicating that the option is required - or not - on the
            command line. If omitted from the yaml, the option is not required to be
            provided by the user. If the option is required, but not provided, then
            a parse error is returned by the ``parse`` function.
default     Non-required options can have a default. If the option is not provided on
            the command line, it is initialized with this default value. A
            non-required option that is not provided and doesn't have a default gets a
            value of ``None`` injected into your class. If the option is a mult-type
            (see below) then you can initialize with an array using valid yaml array
            syntax.
datatype    An optional data type. If you provide a data type then the params are
            validated against the specified type. It's pretty limited at present: int
            float, bool, and date are supported. A date param matches YYYY-MM-DD, or
            MM-DD-YYYY with dots, dashes, or slashes as the separator. If omitted,
            the value is a string.
multi_type  An optional multi type for *param* options. Valid values: ``exactly``,
            ``at-most``, and ``no-limit``. Works in tandem with the *count* key
            below. If *exactly*, then exactly <count> params are expected. Some examples
            are provided in a later section. If *at-most* then at most <count> params
            are parsed. If *no-limit*, then params are parsed until the next option
            is encountered on the command line - or all command line tokens are read.
count       See ``multi-type`` above.
help        Free-form text describing what the option does.
==========  =====================================================================

**Details**
::

    details: >
      The recursion algorithm uses a weighting scheme to determine the
      amount of detailed parsing to perform at any given level of the
      search hierarchy. The following search terms illustrate the
      weighting:

         weight  term
         ------  ------
         1       foo
         2       bar
         3       baz
         4       foobar

The details section is just a place to put more detail than seems appropriate in the *usage* section. Some utilities have really complex options and parameters. For example, if a parameter value is itself a lookup into a table, or if there are many many usage scenarios, and so forth.Embedded newlines in the yaml are preserved (e.g. for tabular formatting if needed.) Otherwise, content is fitted by pycmdparse to the console window width.

**Examples**
::

    examples:
      - example: foo-utility --verbose --exclude fizzbin frobozz
        explanation: >
          Performs a full traversal, with detailed diagnostic
          information displaying to the console, but terminating
          recursion into any hierarchy containing the terms
          'fizzbin', or 'frobozz'.

      - example: >
          foo-utility --verbose --exclude fizzbin frobozz --
          my-saved-search-file
        explanation: >
          Same as the example above, but in this case compares the
          results determined by the utility to the results previously
          generated in the file 'my-saved-search-file' in the current
          working directory. Only the deltas display to the console.
          (Note - the specified file must adhere to the foo-utility's
          stringent formatting requirements.)

      - example: foo-utility -d 42
        explanation: >
          Performs a search with no search term exclusions, and minimal
          (non-verbose) console output. But only recurses to
          a depth of 42.

The *examples* entry contains a list of *example* entries. Examples are just that. They consist of an *example* key, and an *explanation* key. They are displayed below the details section, pretty much as they appear in the yaml.

**Addendum**
::

    addendum: >
      Version 1.2.3, Copyright (C) The Author 2019\n

      In the Public Domain\n

      Github: https://github.com/theauthor/foo-utility

The *addendum* section is for copyright, version, author, license, URL, anything else. Content is displayed as is, fitted to the console window width.