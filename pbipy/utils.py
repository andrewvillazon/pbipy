"""Utility functions and classes used internally by pybi."""

import json
import re

from requests import Response, Session
from requests.exceptions import HTTPError


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


class RequestsMixin:
    """
    Mixin class for http requests and response handling.

    Lets the PowerBI client and Resources use the same functionality for
    making requests and handling the response.

    Mostly requests lib boilerplate with a sprinkling of json parsing.
    """

    def delete(
        self,
        resource: str,
        session: Session,
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

        response = session.delete(resource)

        if response.status_code not in success_codes:
            raise HTTPError(
                f"""Encountered api error. Response: 
                
                {json.dumps(response.json(), indent=True)})"""
            )

    def post(
        self,
        resource: str,
        session: Session,
        payload: dict,
        success_codes: list[int] = [200, 201],
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
        `success_codes` : `list[int]`, optional
            HTTP response status codes that indicate a successful request.
            Status codes not equal to these will raise an `HTTPError`.

        Returns
        -------
        `Response`
            Response generated from the post request.

        Raises
        ------
        `HTTPError`
            If the response status code was not found in `success_codes`.
        """

        response = session.post(resource, json=payload)

        if response.status_code not in success_codes:
            raise HTTPError(
                f"Encountered api error. Response: {json.dumps(response.json(), indent=True)})"
            )

        return response

    def post_raw(
        self,
        resource: str,
        session: Session,
        payload: dict,
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

            return raw

        except Exception as e:
            raise e

    def put(
        self,
        resource: str,
        session: Session,
        payload: dict,
        success_codes: list[int] = [200, 201],
    ) -> None:
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
        `success_codes` : `list[int]`, optional
            HTTP response status codes that indicate a successful request.
            Status codes not equal to these will raise an `HTTPError`.

        Returns
        -------
        `Response`
            requests Response object.

        Raises
        ------
        `HTTPError`
            If the response status code was not found in `success_codes`.
        """

        response = session.put(resource, json=payload)

        if response.status_code not in success_codes:
            raise HTTPError(
                f"""Encountered api error. Response: 
                
                {json.dumps(response.json(), indent=True)})"""
            )

        return response

    def get(
        self,
        resource: str,
        session: Session,
        params: dict = None,
        success_codes: list[int] = [200, 201],
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
        `success_codes` : `list[int]`, optional
            HTTP response status codes that indicate a successful request.
            Status codes not equal to these will raise an `HTTPError`.

        Returns
        -------
        `Response`
            requests Response object.

        Raises
        ------
        `HTTPError`
            If the response status code was not found in `success_codes`.
        """

        response = session.get(resource, params=params)

        if response.status_code not in success_codes:
            raise HTTPError(
                f"""Encountered api error. Response: 
                
                {json.dumps(response.json(), indent=True)})"""
            )

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
