from mastermind.libs.utils import EnumMeta


class DisplayMode(EnumMeta):
    """Enum for the different display modes, which determine how the menu options are displayed."""

    TITLE_ONLY = "TITLE_ONLY"
    VALUE_ONLY = "VALUE_ONLY"
    BOTH = "BOTH"
