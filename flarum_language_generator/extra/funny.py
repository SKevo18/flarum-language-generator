from bs4 import BeautifulSoup
from requests_cache.session import CachedSession



SESSION = CachedSession()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
})


def __funtranslations(original: str, url: str, find_id: str) -> str:
    response = SESSION.post(url, data={"text": original, "submit": ''})
    html = response.text
    parser = BeautifulSoup(html, features="html.parser")

    translated = parser.find(id=find_id)

    return translated.get_text().strip()


def translate_to_lolcat(original: str) -> str:
    return __funtranslations(original, "https://funtranslations.com/lolcat", "lolcat")


def translate_to_pirate(original: str) -> str:
    return __funtranslations(original, "https://funtranslations.com/pirate", "pirate")


if __name__ == "__main__":
    print("LOLCat:", translate_to_lolcat("Quick brown fox jumped over lazy dog on this beautiful sunny day."))
    print("Pirate:", translate_to_pirate("Quick brown fox jumped over lazy dog on this beautiful sunny day."))
