"""Utility functions that are consumed internally by pbipy."""

from pathlib import Path
import re
from typing import TYPE_CHECKING

from requests import RequestException, Response, Session

if TYPE_CHECKING:
    from pbipy.resources import Resource


def build_path(
    path_format: str,
    *identifiers: "str | Resource",
) -> str:
    """
    Build a path to a resource from the supplied components.

    Parameters
    ----------
    `path_format` : `str`
        The resource format with bracketed placeholders, e.g., `reports/{}/datasources`
    `*identifiers` : `str | Resource`
        Ids or Resource Objects with an `id` attribute. The provided Ids
        will be added to the path according `path_format`.

    Returns
    -------
    `str`
        Path to a resource.

    """

    ids = []

    for identifier in identifiers:
        try:
            ids.append(identifier.id)
        except AttributeError:
            ids.append(identifier)

    path = path_format.format(*ids)

    return path


def to_snake_case(s):
    pattern = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
    return pattern.sub(r"_\1", s).lower()


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()

    if len(text) == 0:
        return text

    return s[0] + "".join(i.capitalize() for i in s[1:])


def remove_no_values(
    d: dict,
) -> dict:
    """
    Recursively remove keys with a value of `None` or `{}` from a dictionary.
    If the result of removing `None` is `{}`, then this is removed until
    only keys with values remain.

    Parameters
    ----------
    `d` : `dict`
        dict to remove None or empty dicts from.

    Returns
    -------
    `dict`
        dict with `None` or `{}` removed.
    """

    new_d = {}

    for k, v in d.items():
        if isinstance(v, dict):
            v = remove_no_values(v)
        if not v in (None, {}):
            new_d[k] = v

    return new_d


def file_path_from_components(
    file_name: str,
    extension: str,
    directory: str | Path = None,
):
    """
    Create a file path from file path components.

    Parameters
    ----------
    `file_name` : `str`
        Name of the file (without extension).
    `extension` : `str`
        The file extension.
    `directory` : `str | Path`, optional
        Directory of the file.

    Returns
    -------
    `Path`
        File path to the file.

    """

    if isinstance(directory, str):
        f_dir = Path(directory)
    elif directory is None:
        f_dir = Path()  # cwd
    else:
        f_dir = directory

    # Be a bit more flexible and accept .ext
    if extension[0] == ".":
        f_ext = extension[1:]
    else:
        f_ext = extension

    return f_dir / f"{file_name}.{f_ext}"


def to_identifier(
    s: str,
) -> str:
    """
    Convert a string into a valid Python identifier, e.g., variable or
    attribute name.

    Parameters
    ----------
    `s` : `str`
        String to convert.

    Returns
    -------
    `str`
        Converted string.

    """

    # Remove leading characters until letter or underscore
    s = re.sub("^[^a-zA-Z_]+", "", s)

    # Replace invalid characters
    s = re.sub("[^0-9a-zA-Z_]", "_", s)

    return s


def parse_raw(
    raw: dict,
) -> dict | list[dict]:
    """
    Parses json from an api response.

    Depending on the endpoint, the json will be a dict representing the
    requested object, or a list of dicts at the `"values"` key. If a list,
    this method will return the list, rather than the original json dict.

    Parameters
    ----------
    `raw` : `dict`
        Raw json from the api response.

    Returns
    -------
    `dict | list[dict]`
        Either dict representation of the object, or a list of dict
        representations.

    """

    if "value" in raw:
        return raw["value"]
    else:
        return raw


def raise_error(
    response: Response,
) -> None:
    """
    Wrapper around request's `raise_for_status()` method. Customizes the
    error message to include any extra information provided by the api.

    Parameters
    ----------
    `response` : `Response`
        Requests `Response` object.

    Raises
    ------
    `Exception`
        If there was an error in the response.

    """

    try:
        js = response.json()
    except Exception:
        js = None

    try:
        response.raise_for_status()
    except RequestException as rex:
        if js:
            if len(rex.args) >= 1:
                rex.args = (
                    rex.args[0] + f". Additional information from API: {js}",
                ) + rex.args[1:]

        raise rex


def get(
    resource: str,
    session: Session,
    params: dict = None,
    **kwargs: dict,
) -> Response:
    """
    Get a resource from an api endpoint. Wraps request's `get` method to
    include api-specific error handling.

    Parameters
    ----------
    `resource` : `str`
        URL of the resource.
    `session` : `Session`
        Authenticated `requests.Session` object used to make the request.
    `params` : `dict`, optional
        Request parameters.

    Returns
    -------
    `Response`
        requests `Response` object.

    Raises
    ------
    `Exception`
        If there was an error during the request process.

    """

    try:
        response = session.get(resource, params=params, **kwargs)
        raise_error(response)
    except Exception as ex:
        raise ex

    return response


def get_raw(
    resource: str,
    session: Session,
    params: dict = None,
    **kwargs: dict,
) -> dict | list:
    """
    Convenience function that makes a get request to an api resource, handles
    the response, and returns parsed json.

    Parameters
    ----------
    `resource` : `str`
        URL of the api resource.
    `session` : `Session`
        Authenticated `requests.Session` object used to make the request.

    Returns
    -------
    `dict | list`
        Parsed response json using `_utils.parse_raw`.

    Raises
    ------
    `Exception`
        If there was an error during the request process.

    """

    try:
        response = get(
            resource,
            session,
            params,
            **kwargs,
        )
        raw = response.json()

        return parse_raw(raw)

    except Exception as ex:
        raise ex


def post(
    resource: str,
    session: Session,
    payload: dict = None,
    params: dict = None,
) -> Response:
    """
    Post data to an api endpoint. Wraps request's `post` method to include
    api-specific error handling.

    Parameters
    ----------
    `resource` : `str`
        URL of the resource to post to.
    `session` : `Session`
        Authenticated `requests.Session` object used to make the request.
    `payload` : `dict`, optional
        Data to post to the resource.
    `params` : `dict`, optional
        Request parameters.

    Returns
    -------
    `Response`
        Response generated from the post request.

    Raises
    ------
    `Exception`
        If there was an error during the request process.

    """

    try:
        response = session.post(
            resource,
            params=params,
            json=payload,
        )
        raise_error(response)
    except Exception as ex:
        raise ex

    return response


def post_raw(
    resource: str,
    session: Session,
    payload: dict = None,
    **kwargs: dict,
) -> dict:
    """
    Convenience function that posts to an api endpoint, handles the response,
    and returns parsed json.

    Parameters
    ----------
    `resource` : `str`
        URL of the resource to post to.
    `session` : `Session`
        Authenticated `requests.Session` object used to make the request.
    `payload` : `dict`, optional
        Request data.

    Returns
    -------
    `dict`
        Parsed response json using `_utils.parse_raw`.

    Raises
    ------
    `Exception`
        If there was an error during the request process.

    """

    try:
        response = post(
            resource,
            session,
            payload,
            **kwargs,
        )
        raw = response.json()

        return parse_raw(raw)

    except Exception as ex:
        raise ex


def put(
    resource: str,
    session: Session,
    payload: dict,
) -> Response:
    """
    Make a put request to an api endpoint. Wraps request's `put` method
    to include api-specific error handling.

    Parameters
    ----------
    `resource` : `str`
        URL of the resource.
    `session` : `Session`
        Authenticated `requests.Session` object used to make the request.
    `payload` : `dict`
        Payload data to include with the put request.

    Returns
    -------
    `Response`
        requests Response object.

    Raises
    ------
    `Exception`
        If there was an error during the request process.

    """

    try:
        response = session.put(resource, json=payload)
        raise_error(response)
    except Exception as ex:
        raise ex

    return response


def patch(
    resource: str,
    session: Session,
    payload: dict = None,
) -> Response:
    """
    Make a patch request to an api endpoint. Wraps request's `patch` method
    to include api-specific error handling.

    Parameters
    ----------
    `resource` : `str`
        URL of the resource to patch.
    `session` : `Session`
        Authenticated `requests.Session` object used to make the request.
    `payload` : `dict`
        Data to patch on the resource.

    Returns
    -------
    `Response`
        Response generated from the patch request.

    Raises
    ------
    `Exception`
        If there was an error during the request process.
    """

    try:
        response = session.patch(
            resource,
            json=payload,
        )
        raise_error(response)
    except Exception as ex:
        raise ex

    return response


def delete(
    resource: str,
    session: Session,
    params: dict = None,
) -> Response:
    """
    Make a delete request to an api endpoint. Wraps request's `delete`
    method to include api-specific error handling.

    Parameters
    ----------
    `resource` : `str`
        URL of the resource.
    `session` : `Session`
        Authenticated `requests.Session` object used to make the request.

    Returns
    -------
    `Response`
        Response generated from the delete request.

    Raises
    ------
    `Exception`
        If there was an error during the request process.

    """

    try:
        response = session.delete(
            resource,
            params=params,
        )
        raise_error(response)
    except Exception as ex:
        raise ex

    return response
