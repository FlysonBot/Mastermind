class FStringTemplate:
    """A class to represent a formatted string template."""

    def __init__(self, template: str) -> None:
        """Initialize with a template string."""
        self.template = template

    def eval(self, **kwargs):
        """Evaluate the template with the given keyword arguments."""
        return self.template.format(**kwargs)
