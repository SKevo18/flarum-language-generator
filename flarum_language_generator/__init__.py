from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.absolute()
DEFAULT_FLARUM_VERSION_REGEX = r"^(\^|>|>=)?[1]+.[0x]+.[0-4x]+$"
