from flarum_language_generator.generate_locales import translate_locales
from deep_translator import MyMemoryTranslator


def translate_string_with_mymemory(string: str, target_language_code: str) -> str:
    try:
        translation = MyMemoryTranslator(source='en', target=target_language_code).translate(text=string)

        return translation

    except Exception:
        # If the string couldn't be translated, return the original:
        return string


if __name__ == "__main__":
    LANGUAGES = ['sk', 'cs']

    for language in LANGUAGES:
        print(f"Translating to {language}...")
        translate_locales(to_language=language, translated_directory=f"all/{language}", translate_func=translate_string_with_mymemory)
