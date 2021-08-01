from typing import Callable, Generator, Union

import re

from deep_translator import GoogleTranslator
try:
    from flarum_language_generator.extra.funny import translate_to_lolcat, translate_to_pirate
except:
    pass

YAML_LINE_REGEX = re.compile(r"^( +)([\w\d-]+) *:(?!(?:[\r\n]+| ?(?:\||\|-|>|>-|=>))) ?[\"']?([^\r\n\"'{}]+)[\"']?$")


def translate_string(string: str, target_language_code: str) -> str:
    if target_language_code == "lolcat":
        return translate_to_lolcat(string)
    
    if target_language_code == "pirate":
        return translate_to_pirate(string)

    try:
        translation = GoogleTranslator(source='en', target=target_language_code).translate(text=string)

        return translation

    except Exception:
        # If the string couldn't be translated, return the original:
        return string


def translate_yaml(yaml_text: str, target_language_code: str, translate_func: Callable[[str, str], str]=translate_string, iterator: bool=True) -> Union[str, Generator[str, None, None]]:
    def __translate(to_translate: str) -> Generator[str, None, None]:
        yield "# Automatically translated with https://github.com/CWKevo/flarum-language-generator\n\n"

        for line in to_translate.splitlines(keepends=True):
            match = YAML_LINE_REGEX.match(line)

            if match:
                indent = match.group(1)
                key = match.group(2)
                value = match.group(3)

                if '"' in value:
                    quote = "'"

                else:
                    quote = '"'

                translation = translate_func(value, target_language_code)
                yield f"{indent}{key}: {quote}{translation}{quote} # Original: {value}\n"

            else:
                yield f"{line}"

    if iterator:
        return __translate(yaml_text)

    else:
        full_translation = str()

        for line in __translate(yaml_text):
            full_translation += line

        return full_translation


if __name__ == "__main__":
    data = """askvortsov-categories:
  admin:
    basics:
      categories_label: Categories
    labels:
      keep_tags_nav: Keep the tags page link in the nav sidebar?
      child_bare_icon: Bare child icons?
      compact_mobile_mode: Compact mobile mode
      full_page_desktop: Full page desktop?
      parent_remove_icon: Hide icons for top-level tags?
      parent_remove_description: Hide descriptions for top-level tags?
      parent_remove_stats: Hide stats for top-level tags?
      parent_remove_last_discussion: Hide most recent discussions for top-level tags?
      small_forum_optimized: Optimize for small forums?
    help:
      child_bare_icon: Should icons on child categories be displayed without a circular background?
      full_page_desktop: Should the sidebar nav menu be collapsed to a row (like on the traditional tags page)? This will also hide widgets (such as Friends of Flarum Forum Statistics) from the categories page navbar.
      small_forum_optimized:  This will give more accurate discussion/post counts, but will slow medium and large forums dramatically.
    headings:
      nav: Navigation
      layout: Layout
      parent_display: Parent Category Display
      child_display: Child Category Display
      performance: Performance
    title: Categories Settings

  forum:
    all_categories:
      meta_description_text: All Categories
      meta_title_text: => askvortsov-categories.ref.categories
    header:
      back_to_categories_tooltip: Back to Categories
    index:
      categories_link: => askvortsov-categories.ref.categories
    stat-widgets:
      discussion_label: Discussions
      post_label: Posts
    last_discussion_widget:
      no_discussions: No Discussions (Yet!)

  ref:
    categories: Categories"""

    for line in translate_yaml(data, "sk"):
        print(line, end="")
