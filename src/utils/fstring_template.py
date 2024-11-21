class FStringTemplate:
    def __init__(self, template: str) -> None:
        self.template = template

    def eval(self, **kwargs):
        return self.template.format(**kwargs)
