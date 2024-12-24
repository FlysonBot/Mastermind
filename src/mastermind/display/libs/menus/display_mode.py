from mastermind.libs.utils import EnumMeta


class DisplayMode(EnumMeta):
    """Enum for the different display modes, which determine how the menu options are displayed."""

    KEY_ONLY = "KEY_ONLY"
    VALUE_ONLY = "VALUE_ONLY"
    BOTH = "BOTH"
    FLIPPED = "FLIPPED"
