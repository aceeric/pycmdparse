class Stack:
    """
    A simple stack with some additional functionality that supports
    command-line parsing
    """
    def __init__(self, items):
        """
        Initializes the stack from the passed List such that the
        left-most list item is the top of the stack, and the right-most
        list item is  the bottom of the stack

        :param items: the List to initialize the stack from. If None, then
        the stack is initialized in the empty state
        """
        self.items = []
        if items is not None:
            for item in reversed(items):
                self.items.append(item)

    def __repr__(self):
        return str([item for item in reversed(self.items)])

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def pop_all(self):
        to_return = []
        while self.size() > 0:
            to_return.append(self.pop())
        return to_return

    def has_options(self):
        """
        Checks to see if the stack contains any more options (e.g.
        tokens that start with dash or double dash.)

        :return: True if the stack contains any more options, else False
        """
        remaining_options = [item for item in self.items if item.startswith("-")]
        return len(remaining_options) != 0
