from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.absolute()
CACHED_EXTENSIONS = Path(f"{ROOT_PATH}/cached_extensions.json")

DEFAULT_FLARUM_VERSION_REGEX = r"^(\^|>|>=)?[1]+.[0x]+.[0-4x]+$"
ADDITIONAL_LOCALES = [
    "flarum/mentions",
    "flarum/tags",
    "flarum/subscriptions",
    "flarum/suspend",
    "flarum/pusher",
    "flarum/likes",
    "flarum/sticky",
    "flarum/nicknames",
    "flarum/lock",
    "flarum/flags",
    "flarum/bbcode",
    "flarum/approval",
    "flarum/markdown",
    "flarum/akismet"
]
