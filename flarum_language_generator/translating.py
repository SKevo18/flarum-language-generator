from flarum_language_generator.extra.funny import translate_to_lolcat, translate_to_pirate
from typing import Callable, Union, List

import re
from deep_translator import GoogleTranslator


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


def translate_yaml(yaml_text: str, target_language_code: str, translate_func: Callable[[str, str], str]=translate_string) -> Union[str, None]:
    # FIXME: This is the biggest, inefficient mess. Fixation is appreciated.
    # I am not good with RegEx.
    def __translate(yaml_text: str) -> str:
        line_regex = re.compile(r'''^(\s+)([a-zA-Z_\-0-9]+)(\s+)?:(\s+)?(?:"|')?(?=([^'"]+))(?:"|')?''')
        clean_value_regex = re.compile(r'''^(?!=>|\|-|>-|\||>|\s)+(.+)''')
        bad_value_regex = re.compile(r'''.*(?:{.*}|#).*''')

        new_lines = list() # type: List[str]

        for line in yaml_text.splitlines(keepends=True):
            # Entire key: value pair:
            line_match = line_regex.match(line)
            if line_match:
                # The value:
                value = line_match.group(5)

                # Value doesn't start with that thingies that allows you to go newline ("|", ">", "|-", ">-"):
                clean_match = clean_value_regex.match(value)
                if clean_match:
                    clean_value = clean_match.group(1)

                    # Value contains variables ("{x}" or "#"):
                    if not bad_value_regex.match(clean_value):
                        # Choose correct quotes:
                        if '"' in clean_value:
                            translated = translate_func(clean_value.strip(), target_language_code)
                            new_lines.append(f"{line_match.group(1)}{line_match.group(2)}:{line_match.group(4)}'{translated}' # Original: {clean_value}\n")
                            continue

                        else:
                            translated = translate_func(clean_value.strip(), target_language_code)
                            new_lines.append(f'{line_match.group(1)}{line_match.group(2)}:{line_match.group(4)}"{translated}" # Original: {clean_value}\n')
                            continue

                    else:
                        new_lines.append(line)
                        continue

                else:
                    new_lines.append(line)
                    continue

            else:
                new_lines.append(line)
                continue

        return ''.join(new_lines)


    translated_yaml = __translate(yaml_text)

    return translated_yaml
