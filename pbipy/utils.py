"""Utility functions and classes used internally by pybi."""

import json
from pathlib import Path
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pbipy.resources import Resource

from requests import Response, Session
from requests.exceptions import HTTPError, RequestException


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


class RequestsMixin:
    """
    Mixin class for http requests and response handling.

    Lets the PowerBI client and Resources use the same functionality for
    making requests and handling the response.

    Mostly requests lib boilerplate with a sprinkling of json parsing.
    """

    def _raise_errors(
        self,
        response: Response,
    ) -> None:
        """
        Wrapper around request's `raise_for_status()` method that customizes
        the error if any extra information was provided by the api.

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

    def delete(
        self,
        resource: str,
        session: Session,
        params: dict = None,
        success_codes: list[int] = [200, 201],
    ) -> None:
        """
        Make a delete request to an api endpoint.

        Parameters
        ----------
        `resource` : `str`
            URL of the resource.
        `session` : `Session`
            Requests Session object used to make the request.
        `success_codes` : `list[int]`, optional
            HTTP response status codes that indicate a successful request.
            Status codes not equal to these will raise an `HTTPError`.

        Raises
        ------
        `HTTPError`
            If the response status code was not found in `success_codes`.
        """

        response = session.delete(
            resource,
            params=params,
        )

        if response.status_code not in success_codes:
            raise HTTPError(
                f"""Encountered api error. Response: 
                
                {json.dumps(response.json(), indent=True)})"""
            )

    def patch(
        self,
        resource: str,
        session: Session,
        payload: dict = None,
    ) -> Response:
        """
        Patch a resource.

        Parameters
        ----------
        `resource` : `str`
            URL of the resource to patch.
        `session` : `Session`
            Requests Session object used to make the request.
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
            response = session.patch(resource, json=payload)
            self._raise_errors(response)
        except Exception as ex:
            raise ex

        return response

    def post(
        self,
        resource: str,
        session: Session,
        payload: dict = None,
        params: dict = None,
    ) -> Response:
        """
        Post data to an api endpoint.

        Parameters
        ----------
        `resource` : `str`
            URL of the resource to post to.
        `session` : `Session`
            Requests Session object used to make the request.
        `payload` : `dict`
            Data to post to the resource.

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
            self._raise_errors(response)
        except Exception as ex:
            raise ex

        return response

    def post_raw(
        self,
        resource: str,
        session: Session,
        payload: dict = None,
        **kwargs: dict,
    ) -> dict:
        """
        Make a post request and return any resulting json.

        Parameters
        ----------
        `resource` : `str`
            URL of the resource to post to.
        `session` : `Session`
            Requests Session to use to make the request.
        `payload` : `dict`
            Request data.

        Returns
        -------
        `dict`
            Request json. `response.json()`

        Raises
        ------
        `Exception`
            If encountered error with the request.
        """

        try:
            response = self.post(resource, session, payload, **kwargs)
            raw = response.json()

            return self.parse_raw(raw)

        except Exception as e:
            raise e

    def put(
        self,
        resource: str,
        session: Session,
        payload: dict,
    ) -> Response:
        """
        Make a put request to an api endpoint.

        Parameters
        ----------
        `resource` : `str`
            URL of the resource.
        `session` : `Session`
            Requests Session object used to make the request.
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
            self._raise_errors(response)
        except Exception as ex:
            raise ex

        return response

    def get(
        self,
        resource: str,
        session: Session,
        params: dict = None,
    ) -> Response:
        """
        Get a resource from an api endpoint.

        Parameters
        ----------
        `resource` : `str`
            URL of the resource.
        `session` : `Session`
            Requests Session object used to make the request.
        `params` : `dict`, optional
            Request parameters.

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
            response = session.get(resource, params=params)
            self._raise_errors(response)
        except Exception as ex:
            raise ex

        return response

    def get_raw(
        self,
        resource: str,
        session: Session,
        params: dict = None,
        **kwargs: dict,
    ) -> dict | list:
        """
        Request an api resource, parse the response json, and return the
        parsed json.

        Parameters
        ----------
        `resource` : `str`
            URL of the api resource.
        `session` : `Session`
            Requests Session object used to make the request.

        Returns
        -------
        `dict | list`
            Returns either the dict representation of the resource, or list
            of resources.

        Raises
        ------
        `Exception`
            Error encountered during the request process.
        """

        try:
            response = self.get(resource, session, params, **kwargs)
            raw = response.json()

            return self.parse_raw(raw)

        except Exception as e:
            raise e

    def parse_raw(
        self,
        raw: dict,
    ) -> dict | list[dict]:
        """
        Parses json from an api response.

        Depending on the endpoint, the json will either include a dict
        representation of a single object, or a list of dicts found in
        the "values" key. If a list, this method will return the list,
        rather than the original json dict.

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
