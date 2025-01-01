from enum import Enum


class DisplayMode(Enum):
    """Enum for the different display modes, which determine how the menu options are displayed."""

    TITLE_ONLY = "TITLE_ONLY"  # for when user customized the key rendering
    BOTH = "BOTH"
