"""
Module implements a wrapper around the Power BI Rest API.

Users construct an instance of the PowerBI client and call its methods. These 
methods closely follow the naiming laid out here:

https://learn.microsoft.com/en-us/rest/api/power-bi/
"""

import requests

from pbipy.resources import Dataset


class PowerBI:
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
