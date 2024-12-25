from dataclasses import dataclass


@dataclass
class AllSettings:
    """Collection of all settings for the application. Only True/False settings are supported."""

    EXAMPLE_SETTING: bool = True
