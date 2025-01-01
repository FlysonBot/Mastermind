from mastermind.client.languages.localization import Localization


def example_get_language_preference() -> str:
    return "en"


console_localization = Localization(language="en")  # used for CLI
global_localization = Localization(  # use everywhere else
    language=example_get_language_preference()
)
