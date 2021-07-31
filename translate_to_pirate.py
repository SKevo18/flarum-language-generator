from flarum_language_generator.generate_locales import translate_locales


if __name__ == "__main__":
    print(f"Translating to Pirate...")
    translate_locales(to_language="pirate", translated_directory=f"all/pirate")
