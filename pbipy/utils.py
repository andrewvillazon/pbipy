"""Utility functions used internally by pybi."""

import copy
import json
import re


def camel_to_snake(s):
    pattern = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
    return pattern.sub(r"_\1", s).lower()


def camel_case_dict_keys(d):
    return {camel_to_snake(k): v for k, v in d.items()}


def _convert_js_strings(js):
    for k, v in js.items():
        if isinstance(v, dict):
            _convert_js_strings(v)
        elif isinstance(v, str):
            try:
                js_from_str = json.loads(v)
                js[k] = js_from_str
            except:
                pass


def convert_js_strings(js):
    """
    Recursively traverse a dict and attempt to convert any json-like strings to json.

    Parameters
    ----------
    `js` : `dict`
        Json or dict to traverse and convert

    Returns
    -------
    `dict`
        New dict with json-like strings converted to json.
    """    

    new_js = copy.deepcopy(js)
    _convert_js_strings(new_js)

    return new_js
