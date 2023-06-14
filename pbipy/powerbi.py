"""
Module implements a wrapper around the Power BI Rest API.

Users construct an instance of the PowerBI client and call its methods. These 
methods closely follow the naiming laid out here:

https://learn.microsoft.com/en-us/rest/api/power-bi/
"""

import requests
from pbipy import settings

from pbipy.resources import Dataset


class PowerBI:
    BASE_URL = settings.BASE_URL

    def __init__(
        self,
        bearer_token: str,
        session: requests.Session = None,
    ) -> None:
        self.bearer_token = bearer_token

        if not session:
            self.session = requests.Session()

        self.session.headers.update({"Authorization": f"Bearer {self.bearer_token}"})

    def get_dataset(
        self,
        dataset: str | Dataset,
        group: str = None,
    ) -> Dataset:
        if isinstance(dataset, Dataset):
            return dataset

        dataset = Dataset(dataset, self.session, group_id=group)
        dataset.load()

        return dataset

    def get_datasets(
        self,
        group: str = None,
    ) -> list[Dataset]:
        """
        Returns a list of datasets from MyWorkspace or the specified group.

        Parameters
        ----------
        `group` : str, optional
            Group Id where the datasets reside. If not supplied, then datasets 
            will be retrieved from MyWorkspace.

        Returns
        -------
        `list[Dataset]`
            List of datasets for MyWorkspace or the specified group.
        """

        if group:
            path = f"groups/{group}/datasets"
        else:
            path = "datasets"

        resource = self.BASE_URL + path
        response = self.session.get(resource)
        js = response.json()

        if js["value"] == []:
            return []

        datasets = [
            Dataset(
                dataset_js.get("id"),
                self.session,
                group_id=group,
                raw=dataset_js,
            )
            for dataset_js in js["value"]
        ]

        return datasets
