import json
from pathlib import Path
from typing import Any, Dict

from mastermind.libs.utils import CallableDotDict

JSON = list[Any] | dict[str, Any]


class Localization:
    """Localization class for printing messages in different languages."""

    _language_pack: Dict[str, CallableDotDict] = {}

    def __init__(self, language: str = "en") -> None:
        self.language = language  # call the setter to load the language pack

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        self.messages: CallableDotDict = self.load_language_pack(language)
        self._language: str = language

    def load_language_pack(self, language: str) -> CallableDotDict:
        if language in self._language_pack:
            return self._language_pack[language]

        file_path = Path(f"{Path(__file__).parent}/{language}.json")
        if not file_path.is_file():
            raise FileNotFoundError(f"Language pack for '{language}' not found.")

        with open(file_path, "r", encoding="utf-8") as f:

            def print_message(message: str, **kwargs: Any) -> str:
                return message.format(**kwargs)

            data: JSON = json.load(f)
            self._language_pack[language] = CallableDotDict(data, func=print_message)
            return self._language_pack[language]

    def __getattr__(self, item: str) -> CallableDotDict:
        return getattr(self.messages, item)
