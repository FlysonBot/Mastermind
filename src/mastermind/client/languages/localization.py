import json
from pathlib import Path
from typing import Any, Dict

from mastermind.libs.logs import ClientLogger
from mastermind.libs.utils import CallableDotDict

JSON = list[Any] | dict[str, Any]
logger = ClientLogger("Localization")


class Localization:
    """Localization class for printing messages in different languages.

    Examples:
        >>> localization = Localization(language="en")
        >>> localization.language
        'en'
        >>> localization.menu.main_menu.menu_title
        'Main Menu'
        >>> localization.language = "zh"
        >>> localization.menu.main_menu.menu_title
        '主菜单'
        >>> localization.language = "unsupported_language"
        Traceback (most recent call last):
        ...
        FileNotFoundError: Language pack for 'unsupported_language' not found.
    """

    _language_pack: Dict[str, CallableDotDict] = {}

    def __init__(self, language: str = "en") -> None:
        self.language = language  # call the setter to load the language pack

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        """Set and load new language."""
        logger.debug(f"Setting language to: {language}")
        self.messages: CallableDotDict = self.load_language_pack(language)
        self._language: str = language

    def load_language_pack(self, language: str) -> CallableDotDict:
        """Load specified language pack from file."""
        if language in self._language_pack:
            return self._language_pack[language]

        file_path = Path(f"{Path(__file__).parent}/{language}.json")
        if not file_path.is_file():
            logger.error(f"Language pack for '{language}' not found.")
            raise FileNotFoundError(f"Language pack for '{language}' not found.")

        with open(file_path, "r", encoding="utf-8") as f:

            def print_message(message: str, **kwargs: Any) -> str:
                return message.format(**kwargs)

            data: JSON = json.load(f)
            self._language_pack[language] = CallableDotDict(data, func=print_message)
            logger.info(f"Language pack for '{language}' loaded successfully")
            return self._language_pack[language]

    def __getattr__(self, item: str) -> CallableDotDict:
        return getattr(self.messages, item)
