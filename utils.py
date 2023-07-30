import re


def break_string(x):
    pattern = r'(\d+)(\D+)'
    matches = re.match(pattern, x)
    number = matches.group(1)
    characters = matches.group(2)

    return number, characters
