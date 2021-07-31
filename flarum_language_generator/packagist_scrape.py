from typing import Generator, Union, List, Dict

import re

from requests_cache import CachedSession
from flarum_language_generator import ROOT_PATH, DEFAULT_FLARUM_VERSION_REGEX

SESSION = CachedSession(cache_name=f"{ROOT_PATH}/cache/cached_requests.sql")


class FlarumExtension(dict):
    @property
    def name(self) -> Union[str, None]:
        x = self.get("name", None)

        return x


    @property
    def flarum_name(self) -> str:
        return self.name.replace('/', '-')


    @property
    def github_id(self) -> Union[str, None]:
        x = self.get("source", {}).get("url", None) # type: str

        if x:
            return '/'.join(x.split('/')[-2:]).replace(".git", '')

        else:
            return None


    @property
    def abandoned(self) -> Union[str, bool, None]:
        x = self.get("abandoned", None)

        # Sometimes, the abandoned key is an empty string:
        if x is not None and len(x) > 0:
            return x

        else:
            return False


    @property
    def flarum_version(self) -> Union[str, None]:
        return self.get("require", {}).get("flarum/core", None)


def get_all_extensions(flarum_version_regex: Union[str, re.Pattern]=DEFAULT_FLARUM_VERSION_REGEX, include_core: bool=True) -> Generator[FlarumExtension, None, None]:
    packagist_data = SESSION.get("https://packagist.org/packages/list.json?type=flarum-extension").json() # type: Dict[str, List[str]]
    extensions = packagist_data.get("packageNames", [])


    if not isinstance(flarum_version_regex, re.Pattern):
        version_regex = re.compile(flarum_version_regex)

    else:
        version_regex = flarum_version_regex


    if include_core:
        extensions.append("flarum/core")


    for extension_name in extensions:
        data = SESSION.get(f"https://repo.packagist.org/p2/{extension_name}.json").json() # type: dict
        extension = data.get("packages", {}).get(extension_name, None)

        if extension:
            parsed_extension = FlarumExtension(extension[0])

            if parsed_extension.flarum_version:
                if version_regex.match(parsed_extension.flarum_version):

                    yield parsed_extension

                else:
                    continue

            else:
                continue

        else:
            continue

