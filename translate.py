from flarum_language_generator.generate_locales import translate_locales


if __name__ == "__main__":
    LANGUAGES = ['sk', 'cs', 'lolcat', 'pirate']

    for language in LANGUAGES:
        print(f"Translating to {language}...")
        translate_locales(to_language=language, translation_directory=f"all/{language}")
