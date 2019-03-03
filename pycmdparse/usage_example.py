class UsageExample:
    """
    Supports providing a usage example to help the end user. In cases with complex
    functionality and lots of options/params, an example can help the user get started. An
    example consists of two parts: one part showing a command line exemplar, and a second
    part consisting of a narrative that explains the result. E.g.:

    First part:
    my-utility --verbose --log-file=~/tmp/my-utility.log --log-cat=WARN --append

    Second part:
    Gathers system diagnostics, producing data to the log file '~/tmp/my-utility.log'.
    Logging is verbose, meaning detailed diagnostic information is included. As
    specified by the --log-cat option, only warnings are logged. Content is appended to
    the file. (If --append were omitted, then the file would be overwritten each time.)
    """
    def __init__(self, example):
        """
        Initializes the instance from the passed dictionary. The dictionary is expected to
        have been produced from yaml. The yaml spec for an example is:

        examples:
          - example: foo-utility FROM TO
            explanation: >
              Reads from file FROM and writes to file TO

        :param example: According the the spec above, this would be a single example's
        dictionary, containing two keys: "example", and "explanation"
        """
        self._example = example.get("example")
        self._explanation = example.get("explanation")

    @property
    def example(self):
        return self._example

    @property
    def explanation(self):
        return self._explanation
