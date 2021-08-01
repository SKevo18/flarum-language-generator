from typing import Generator, Optional, Union, List, Dict

import re

from requests_cache import CachedSession
from flarum_language_generator import ROOT_PATH, DEFAULT_FLARUM_VERSION_REGEX

SESSION = CachedSession(cache_name=f"{ROOT_PATH}/cache/cached_packagist_requests.sql")
GITHUB_ID_REGEX = re.compile(r'(?:https:|http:)\/\/github\.com\/([\w\d-]+\/[.\w\d-]+).git')


class FlarumExtension(dict):
    def __repr__(self) -> str:
        return self.name


    @property
    def name(self) -> str:
        x = self.get("name", None) # type: str

        if x:
            return x.lower()


    @property
    def flarum_name(self) -> str:
        return self.name.replace('/', '-')


    @property
    def github_id(self) -> Optional[str]:
        x = self.get("source", {}).get("url", None) # type: str

        if x:
            match = GITHUB_ID_REGEX.match(x)

            if match:
                return match.group(1)


    @property
    def abandoned(self) -> Optional[Union[str, bool]]:
        x = self.get("abandoned", None)

        # Sometimes, the abandoned key is an empty string:
        if x is not None and len(x) > 0:
            return x

        else:
            return False


    @property
    def flarum_version(self) -> Optional[str]:
        return self.get("require", {}).get("flarum/core", None)


def get_extension_list():
    packagist_data = SESSION.get("https://packagist.org/packages/list.json?type=flarum-extension").json() # type: Dict[str, List[str]]
    extensions = packagist_data.get("packageNames", []) # type: list

    return extensions


def get_all_extensions(flarum_version_regex: Union[str, re.Pattern]=DEFAULT_FLARUM_VERSION_REGEX) -> Generator[FlarumExtension, None, None]:
    extensions = get_extension_list()


    if not isinstance(flarum_version_regex, re.Pattern):
        version_regex = re.compile(flarum_version_regex)

    else:
        version_regex = flarum_version_regex


    def __get_extension(extension_name: str) -> FlarumExtension:
        try:
            data = SESSION.get(f"https://repo.packagist.org/p2/{extension_name}.json").json() # type: dict
            extension = data.get("packages", {}).get(extension_name, None)

        except ConnectionError as error:
            print(f"ConnectionError raised when obtaining {extension_name}, skipping... | ", error)
            return None

        if extension:
            parsed_extension = FlarumExtension(extension[0])

            if parsed_extension.flarum_version:
                if version_regex.match(parsed_extension.flarum_version):
                    return parsed_extension


    for extension_name in extensions:
        try:
            extension = __get_extension(extension_name)

            if extension:
                yield extension

        except ConnectionError as error:
            print(f"ConnectionError for extension {extension_name}:", error)
