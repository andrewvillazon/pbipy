"""Utility functions used internally by pybi."""

import re


def to_snake_case(s):
    pattern = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
    return pattern.sub(r"_\1", s).lower()


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    
    if len(text) == 0:
        return text
    
    return s[0] + ''.join(i.capitalize() for i in s[1:])
