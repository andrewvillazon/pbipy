"""
Module implements a wrapper around the Power BI Rest API.

Users construct an instance of the PowerBI client and call its methods. These 
methods closely follow the naiming laid out here:

https://learn.microsoft.com/en-us/rest/api/power-bi/
"""

import requests

from .operationgroups import Datasets
from .operationgroups import Groups


class PowerBI:
    """
    User Interface into Power BI Rest Api.

    Users interact with their Power BI service by constructing an instance of this
    object and calling its methods.

    Authentication with the Power BI service requires a `bearer_token` which must be
    generated in advance before creating the `PowerBI` object. How you generate the token
    will depend on your Azure and Power BI configuration.

    In general, `PowerBI()` methods follow the naming laid out here:

    https://learn.microsoft.com/en-us/rest/api/power-bi/

    Parameters
    ----------
    `bearer_token` : `str`
        Bearer token used to authenticate with your Power BI service.
    """

    def __init__(self, bearer_token, session=None):
        self.bearer_token = bearer_token

        if not session:
            self.session = requests.Session()

        self.session.headers.update({"Authorization": f"Bearer {self.bearer_token}"})

        self.datasets = Datasets(self)
        self.groups = Groups(self)

    def _get_resource(self, url_format, *id, parameters={}):
        """
        Fetch a resource from the Power BI Rest API.

        Takes a templated url, id(s) used in the resource, and optional
        parameters. Constructs the url to the resource and requests the
        resource from the Power BI Rest API. Returns the associated response.

        If the response contains a list of Power BI objects, this will be
        parsed and the list of objects returned.

        Parameters
        ----------
        `url_format` : `str`
            The url of the resource. May also include placeholders,
            e.g., `datasets/{datasetId}/refreshes`.
        `*id` : `tuple`
            Id values to include in the url. Any placeholders in
            `url_format` will be replaced with these values in the
            order they are passed in.
        `**parameters`: `dict`
            Keyword argument of optional url parameters, e.g.,
            `$top` to limit number of results returned.


        Returns
        -------
        `json`
            The json response as returned from the api call. Where the api response contains
            a list of objects, e.g., a list of Datasets, the response will be parsed to only
            return this list.
        """

        if id:
            if isinstance(id, tuple):
                url = url_format.format(*id)
            else:
                url = url_format.format(id)
        else:
            url = url_format

        resp = self.session.get(url, params=parameters)
        raw = resp.json()

        # NOTE: Will we need this in future?
        if "@odata.context" in raw:
            del raw["@odata.context"]

        if "value" in raw:
            if isinstance(raw["value"], list):
                raw = raw["value"]

        return raw
    

    