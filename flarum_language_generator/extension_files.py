import time

from requests_cache import CachedSession
from flarum_language_generator import ROOT_PATH

GITHUB_URL = "https://raw.githubusercontent.com/{github_id}/master"
SESSION = CachedSession(cache_name=f"{ROOT_PATH}/cache/cached_requests.sql")


def get_locale_file(github_id: str, language_code: str="en", max_retries: int=3, delay_between_retries: float=10) -> str:
    possible_locations = [
        f"{GITHUB_URL.format(github_id=github_id)}/locale/{language_code}.yml",
        f"{GITHUB_URL.format(github_id=github_id)}/resources/locale/{language_code}.yml"
    ]

    def __try_text(url: str, current_retries: int=0) -> bool:
        response = SESSION.get(url)

        if response.status_code == 200:
            return response.text


        elif response.status_code == 404:
            return None


        else:
            if current_retries < max_retries:
                print(f"{response.status_code} when obtaining {github_id}, retrying again in {delay_between_retries} seconds...")

                current_retries += 1
                time.sleep(delay_between_retries)

                return __try_text(url, current_retries)
            
            else:
                print(f"Failed to obtain locale for {github_id} - tried {current_retries} times, skipping...")

                return None
            


    def __try_possible():
        for possible in possible_locations:
            possible_locale_file = __try_text(possible)

            if possible_locale_file:
                return possible_locale_file

            else:
                continue


    return __try_possible()


if __name__ == "__main__":
    print(get_locale_file("flarum/core", "core"))
