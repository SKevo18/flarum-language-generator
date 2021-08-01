from typing import List

import json
import re

from flarum_language_generator import ROOT_PATH
from flarum_language_generator.packagist_scrape import FlarumExtension, get_all_extensions


def cache_extensions() -> List[str]:
    ver = re.compile(r'^\^?[1]+.[0x]+.[0-4x]+$')


    print("Building valid extension list...")
    valid_extensions = list() # type: List[FlarumExtension]

    for extension in get_all_extensions(ver):
        gid = extension.github_id

        if extension and gid:
            print(f"Found {gid}")
            valid_extensions.append(gid)


    with open(f'{ROOT_PATH}/cached_extensions.json', 'w') as cached_extensions:
        json.dump(list(valid_extensions), cached_extensions, indent=4)

    print(f"Successfuly saved extension list to {ROOT_PATH}/cached_extensions.json")
    return valid_extensions


if __name__ == '__main__':
    print(cache_extensions())
