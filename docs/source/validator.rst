You will likely have custom validation that you need to perform on your command line options. For example, you might enforce that an option value belongs to a list of valid values. Or you might require a file to exist, etc.

``pycmdparse`` provides a validator call back. If you define a function in your subclass that matches this signature:

.. code-block:: python

    @classmethod
    def validator(cls, to_validate):

...then once all built-in validations have passed, your validator will be called to validate each option, as well as the positional params. Here's a skeleton showing how to get started:

.. code-block:: python

    @classmethod
    def validator(cls, to_validate):
        some_error_condition = False
        if isinstance(to_validate, PositionalParams):
            if some_error_condition:
                return OptAcceptResultEnum.ERROR, "TODO message"
        elif isinstance(to_validate, AbstractOpt):
            if to_validate.opt_name == "your_field":
                if some_error_condition:
                    return OptAcceptResultEnum.ERROR, "TODO message"
        return None,

You can see that there is one if block to validate the positional params, and one if block to validate options. Your callback will be called once for each option, and once for the list of positional params. So, for example, you could enforce a specific number of positional params, etc.

Your callback is expected to return a tuple. If your validation fails, then element zero is ``OptAcceptResultEnum.ERROR`` as shown, and element one is a message. If there is no error, then a tuple is returned with ``None`` in element zero.

If your callback returns an error, then you'll pick that up in the return value from your call to the ``parse`` function, and it will be handled the same way as if the library determined that the command line didn't parse successfully.

**Example**
::

    class MyCmdLine(CmdLine):
        yaml_def = '''
        utility:
          name: my-util
        supported_options:
          - category:
            options:
            - name      : it_hurts
              long      : it-hurts
              opt       : param
              multi_type: exactly
              count     : 1
        '''

        it_hurts = None

        @classmethod
        def validator(cls, to_validate):
            if isinstance(to_validate, AbstractOpt):
                if to_validate.opt_name == "it_hurts":
                    if it_hurts == "When I go like this":
                        return OptAcceptResultEnum.ERROR,
                           "Don't go like that"
            return None,

    if __name__ == "__main__":
        parse_result = MyCmdLine.parse(sys.argv)
        if parse_result.value != ParseResultEnum.SUCCESS.value:
            MyCmdLine.display_info(parse_result)
            exit(1)

In this example, the following command line:
::

    my-util --it-hurts='When I go like this'

Would produce the following output:
::
    Error:

    Don't go like that

    For usage instructions, try: my-util -h (or my-util --help)

