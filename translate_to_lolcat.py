from flarum_language_generator.generate_locales import translate_locales


if __name__ == "__main__":
    print(f"Translating to LOLCat...")
    translate_locales(to_language="lolcat", translated_directory=f"all/lolcat")
