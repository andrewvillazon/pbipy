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
    ) -> dict | None:
        response = session.post(resource, json=payload)

        if response.status_code not in success_codes:
            raise HTTPError(
                f"Encountered api error. Response: {json.dumps(response.json(), indent=True)})"
            )

        return response

    def get(
        self,
        resource: str,
        session: Session,
        params: dict = None,
        success_codes: list[int] = [200, 201],
    ) -> Response:
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
        **kwargs: dict,
    ) -> dict | list:
        try:
            response = self.get(resource, session, **kwargs)
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
