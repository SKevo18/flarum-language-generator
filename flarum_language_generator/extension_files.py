from requests_cache import CachedSession
from flarum_language_generator import ROOT_PATH

GITHUB_URL = "https://raw.githubusercontent.com/{extension}/master"
SESSION = CachedSession(cache_name=f"{ROOT_PATH}/cache/cached_requests.sql")


def get_locale_file(extension: str, language_code: str="en") -> str:
    def __try_url(url: str) -> bool:
        try_url = SESSION.get(url)

        if try_url.status_code == 200:
            return True

        else:
            return False

    def __check_exists() -> bool:
        try_url = __try_url(url=f"{GITHUB_URL.format(extension=extension)}/locale/{language_code}.yml")
        if not try_url:
            try_url = __try_url(url=f"{GITHUB_URL.format(extension=extension)}/resources/locale/{language_code}.yml")
            if not try_url:
                return ''

            else:
                return f"{GITHUB_URL.format(extension=extension)}/resources/locale/{language_code}.yml"

        else:
            return f"{GITHUB_URL.format(extension=extension)}/locale/{language_code}.yml"


    url = __check_exists()
    if len(url) > 0:
        return SESSION.get(url).text

    else:
        return None


if __name__ == "__main__":
    print(get_locale_file("flarum/core", "core"))
