class FStringTemplate:
    """
    A class that provides a simple wrapper around the built-in format() method to enable the use of f-strings.

    Attributes:
        template (str): The template string to be used for formatting.
    """

    def __init__(self, template: str) -> None:
        """
        Initializes the FStringTemplate object with the given template string.

        Args:
            template (str): The template string to be used for formatting.
        """
        self.template = template

    def eval(self, **kwargs):
        """
        Evaluates the template string with the given keyword arguments and returns the formatted string.

        Args:
            **kwargs: The keyword arguments to be used for formatting the template string.

        Returns:
            str: The formatted string.
        """
        return self.template.format(**kwargs)
