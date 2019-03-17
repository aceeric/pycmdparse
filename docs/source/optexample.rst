This section presents some examples of defining options in the yaml, and the resulting behavior of the library.

**The bare minimum**
::
    supported_options:
      - category:
        options:
        - long: max-threads

The only key provided is the long option. So this will match ``--max-threads`` on the command line, and will be defined as a param option taking exactly one parameter. So the command line could look like: ``--max-threads=1``, or ``--max-threads 1``. If the command line looked like ``--max-threads``, that would be a parse error. The field name injected into your subclass would be: ``max_threads`` and it would contain a scalar value. You would access the value thus:

.. code-block:: python

    # if cmd line is --max-threads=1, then prints "Max Threads=1":
    print("Max Threads={}".format(MyCmdLine.max_threads))

**A bool, with an explicit name, and both short and long forms**
::
    supported_options:
      - category:
        options:
        - name:  wax_on
          short: w
          long : wax-on
          opt  : bool

Matches ``--wax-on`` and ``-w`` on the command line. Always optional on the command line, because bool options are never required. Has a value of false if omitted from the command line, and a value of true if provided on the command line. The field name injected into your subclass would be: ``wax_on`` as explicitly defined, and it would contain a bool value, and would never have a value of ``None``. You would access the value thus:

.. code-block:: python

    # if cmd line is --wax-on then prints "Wax On":
    if MyCmdLine.wax_on:
        print("Wax On")
    else:
        print("Wax Off")

**A parm, taking exactly one value**
::
    supported_options:
      - category:
        options:
        - name    : depth
          short   : d
          long    : depth
          hint    : n
          required: false
          datatype: int
          opt     : param
          default : 1

In the usage instructions, the option displays like: ``-d,--depth <n>`` indicating that a single parameter is required that's probably a number ("n"). Since neither the *multi-type* key, nor the *count* key are specified, this defaults to an EXACTLY ONE param option. Meaning: when the command line is parsed, exactly one param is expected. So: ``-d 1`` would be valid. But this would be a parse error: ``-d``.

Let's say you didn't define positional params. In this case, ``-d 4 5 6`` would also be a parse error. The reason is, the parser would initialize your option with the value 4, then "5" and "6" would not belong to anything so that would trigger a parse error. If, on the other hand, you did define positional params, then "5" and "6" would get assigned to the positional params because the rule is - after all options are parsed, everything left goes into positional params.

If the command line looked like this: ``-d=123`` then you would access the value thus:

.. code-block:: python

    print("Your depth plus ten is: " + str(MyCmdLine.depth + 10))

**A parm, taking exactly three values**
::
    supported_options:
      - category:
        options:
        - name      : takes_3
          short     : t
          long      : takes-three
          opt       : param
          multi_type: exactly
          count     : 3
          default   :
            - ONE
            - TWO
            - THREE

This example is a param option taking three params. It's initialized with defaults. Since ``required`` is not specified, the option is not required on the command line. Let's say, in this example, that positional params are also defined. Then this is a valid command line: ``--takes-three A B C 'this is a positional param'``. The parse stops as soon as it receives three params. You would access the field in your subclass like this:

.. code-block:: python

    if len(MyCmdLine.takes_3) >= 1:
        print("First Param: " + MyCmdLine.takes_3[0])
    if len(MyCmdLine.takes_3) >= 2:
        print("Second Param: " + MyCmdLine.takes_3[1])
    if len(MyCmdLine.takes_3) >= 3:
        print("Third Param: " + MyCmdLine.takes_3[2])

(Note - the following command-line form is also supported for options taking multiple params: ``--takes-three A --takes-three B --takes-three C``.) One additional thing to note about EXACTLY params is - the tokens pulled from the command line are not examined. So, if the command line looks like: ``--takes-three A --foo --bar`` then the value  of the option will be ``["A", "--foo", "--bar"]``

The reiterate, the field value injected into your subclass is a scalar for cases where the param only takes one value, and a list for cases where the param takes more than one value - as defined in the yaml. In list cases, if no params are provided and no default is defined and the option is not required, then the field value will be an empty list, vs. ``None``.

**A parm, taking at most three values**
::
    supported_options:
      - category:
        options:
        - name      : at_most_3
          long      : at-most-3
          opt       : param
          multi_type: at-most
          count     : 3

For ``at-most`` and ``no-limit`` *multi-type* params, the presence of the next option stops the parser from assigning parameter values to the current option. So, the following command line would be valid: ``--at-most-3 ONE TWO -- POSITIONAL``. Or, if there was another option ``--foo`` that was supported, then this would be a valid command line: ``--at-most-3 ONE TWO --foo``. In this case: ``--at-most-3 ONE TWO THREE POSITIONAL``, the param picks up the values "ONE", "TWO", and "THREE" and stops gathering tokens from the command line, leaving the value "POSITIONAL" for positional params.

**A parm, taking unlimited values**
::
    supported_options:
      - category:
        options:
        - long      : touch-type
          opt       : param
          multi_type: no-limit

In this example, the command line can contain any number of params for this option, and as for the ``at-most`` case, the next option, or the positional params option terminates collection of params:

``--touch-type The quick brown fox jumps over the lazy dog -- positional params``