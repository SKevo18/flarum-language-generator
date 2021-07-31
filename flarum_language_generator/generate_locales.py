from typing import Callable, Generator
from typing import Union, List

import os
import re
import json

from flarum_language_generator.translating import translate_string, translate_yaml
from flarum_language_generator import DEFAULT_FLARUM_VERSION_REGEX, ROOT_PATH
from flarum_language_generator.extension_files import get_locale_file
from flarum_language_generator.packagist_scrape import FlarumExtension, get_all_extensions


def make_dirs(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def scrap_locales(directory_name: str="all", cached_extension_json: Union[str, None]=None, flarum_version_regex: Union[str, re.Pattern]=DEFAULT_FLARUM_VERSION_REGEX):
    result_path = f"{ROOT_PATH}/generated/{directory_name}"
    make_dirs(result_path)


    if cached_extension_json:
        extensions = json.load(open(cached_extension_json, 'r'))

    else:
        extensions = get_all_extensions(flarum_version_regex=flarum_version_regex)
    extensions: Union[Generator[FlarumExtension, None, None], List[FlarumExtension]]


    for extension in extensions:
        name = extension.name

        if os.path.exists(f"{result_path}/{extension.flarum_name}.yml"):
            print(f"{name} is already scrapped, skipping.")
            continue

        # Core uses "core.yml" instead of "en.yml":
        if name == "flarum/core":
            text = get_locale_file("flarum/core", "core")
            result_file_path = f"{result_path}/core.yml"

        else:
            text = get_locale_file(extension.github_id, "en")
            if text:
                id = text.splitlines(keepends=True)[0].strip("\r\n:")
                result_file_path = f"{result_path}/{id}.yml"

        if text:
            print(f"Obtained {name}, writing...")
            with open(result_file_path, "w", encoding='UTF-8') as result_file:
                result_file.write(text)
                continue

        else:
            print(f"Couldn't obtain locale of {name}, skipping...")
            continue


def translate_locales(to_language: str="sk", directory_name: str="all", translated_directory: str="all", translate_func: Callable[[str, str], str]=translate_string):
    translation_dir = f"{ROOT_PATH}/translated/{translated_directory}"
    make_dirs(translation_dir)

    for file in os.listdir(f"{ROOT_PATH}/generated/{directory_name}"):
        if os.path.exists(f"{translation_dir}/{file}"):
            print(f"{file} is already translated, skipping.")
            continue

        if file.endswith(".yml"):
            with open(f"{ROOT_PATH}/generated/{directory_name}/{file}", 'r', encoding='UTF-8') as file_to_translate:
                print(f"Now reading: {file}")
                to_translate = file_to_translate.read()

            with open(f"{translation_dir}/{file}", "w", encoding='UTF-8') as translated_file:
                print(f"Translating {file} (this will take a while)...")
                translated = translate_yaml(to_translate, to_language, translate_func)

                if translated:
                    translated_file.write(translated)

                else:
                    translated_file.write(to_translate)
