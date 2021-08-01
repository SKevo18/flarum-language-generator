from typing import Callable, Generator, Tuple, Union, List

import os
import re
import json

from pathlib import Path

from flarum_language_generator.translating import translate_string, translate_yaml
from flarum_language_generator import ADDITIONAL_LOCALES, DEFAULT_FLARUM_VERSION_REGEX, ROOT_PATH, CACHED_EXTENSIONS
from flarum_language_generator.extension_files import get_locale_file
from flarum_language_generator.packagist_scrape import FlarumExtension, get_all_extensions


ID_REGEX = re.compile(r'^(?!core)([\w\d-]+):$', re.MULTILINE)


def scrap_locales(directory_name: str="all", cached_extension_json: Union[str, None]=CACHED_EXTENSIONS, flarum_version_regex: Union[str, re.Pattern]=DEFAULT_FLARUM_VERSION_REGEX, additional_locales: List[str]=ADDITIONAL_LOCALES):
    result_dir = Path(f"{ROOT_PATH}/generated/{directory_name}")
    os.makedirs(result_dir, exist_ok=True)


    if cached_extension_json is not None:
        extensions = json.load(open(cached_extension_json, 'r')) # type: List[FlarumExtension]

    else:
        extensions = get_all_extensions(flarum_version_regex=flarum_version_regex)


    def __write_locale(locale_id, locale_file):
        locale_location = Path(f"{result_dir}/{locale_id}.yml")

        with open(locale_location, 'w', encoding='UTF-8') as locale_yml:
            locale_yml.write(locale_file)
            print(f"Successfuly wrote {locale_id}.")

            return None


    def __grab_locale(github_id: str) -> Tuple[str, str]:
        locale_file = get_locale_file(github_id)

        if locale_file:
            locale_match = ID_REGEX.search(locale_file)

            if locale_match:
                locale_id = locale_match.group(1)

                return locale_id, locale_file
            
            else:
                print(f"Couldn't obtain ID of locale for {github_id}")
                return None

        else:
            print(f"Couldn't obtain locale for {github_id}, it might not exist or is located elsewhere.")
            return None


    def __locale_generator() -> Generator[Tuple[str, str], None, None]:
        if additional_locales:
            for locale in additional_locales:
                print(f"Obtaining additional locale for {locale}...")
                
                pair = __grab_locale(locale)
                if pair:
                    yield pair


        for extension in extensions:
            print(f"Obtaining locale for {extension}...")

            if isinstance(extension, FlarumExtension):
                pair = __grab_locale(extension.github_id)

            else:
                pair = __grab_locale(extension)

            if pair:
                yield pair


    print("Writing core locale...")
    __write_locale("core", get_locale_file("flarum/core", "core"))

    for locale_id, locale_file in __locale_generator():
        if os.path.exists(Path(f"{result_dir}/{locale_id}.yml")):
            print(f"{locale_id} is already scrapped, skipping...")
            continue

        __write_locale(locale_id, locale_file)



def translate_locales(to_language: str="sk", translate_from: str="all", translation_directory: str="all", translate_func: Callable[[str, str], str]=translate_string, lazy: bool=True):
    from_dir = f"{ROOT_PATH}/generated/{translate_from}"
    translation_dir = f"{ROOT_PATH}/translated/{translation_directory}"
    os.makedirs(translation_dir, exist_ok=True)

    for file in os.listdir(from_dir):
        if os.path.exists(f"{translation_dir}/{file}"):
            print(f"{file} is already translated, skipping.")
            continue

        if file.endswith(".yml"):
            with open(f"{from_dir}/{file}", 'r', encoding='UTF-8') as file_to_translate:
                print(f"Now reading: {file}")
                to_translate = file_to_translate.read()

                with open(f"{translation_dir}/{file}", "w", encoding='UTF-8') as translated_file:
                    print(f"Translating {file}...")

                    if lazy:
                        for line in translate_yaml(to_translate, to_language, translate_func, iterator=True):
                            translated_file.write(line)

                    else:
                        translated = translate_yaml(to_translate, to_language, translate_func, iterator=False)

                        translated_file.write(translated)

                    print(f"{file} was translated successfuly!")
