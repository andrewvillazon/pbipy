import json
from requests.exceptions import HTTPError

from pbipy import settings
from pbipy.utils import RequestsMixin, to_snake_case


class Resource(RequestsMixin):
    BASE_URL = settings.BASE_URL

    def __init__(self, path, session, **kwargs) -> None:
        self.path = path
        self.url = self.BASE_URL + self.path
        self.session = session
        self.raw = None

        if "group_id" in kwargs:
            group_id = kwargs.get("group_id")
            setattr(self, "group_id", group_id)

    def _load_from_raw(self, raw):
        self.raw = raw

        for k, v in raw.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)

        return self

    def load(self):
        response = self.session.get(self.url)
        raw = response.json()

        self._load_from_raw(raw)


class Dataset(Resource):
    def __init__(
        self,
        id,
        session,
        group_id=None,
        raw=None,
    ) -> None:
        self.id = id

        if group_id:
            path = f"groups/{group_id}/datasets/{id}"
        else:
            path = f"datasets/{id}"

        super().__init__(path, session, group_id=group_id)

        # Supports creating from a list of js, e.g., get_datasets endpoint
        if raw:
            self._load_from_raw(raw)

    def get_refresh_history(
        self,
        top: int = None,
    ) -> list[dict]:
        """
        Returns the refresh history for the dataset.

        Parameters
        ----------
        `top` : `int`, optional
            The requested number of entries in the refresh history. If
            not provided, the default is the last available 500 entries.

        Returns
        -------
        `list[dict]`
            List of refresh history entries.

        Raises
        ------
        `HTTPError`
            If the api response status code is not equal to 200.
        """
        # TODO: implement Refresh object

        if self.group_id:
            path = f"groups/{self.group_id}/datasets/{self.id}/refreshes"
        else:
            path = f"datasets/{self.id}/refreshes"

        resource = self.BASE_URL + path
        params = {"$top": top}

        response = self.session.get(resource, params=params)
        raw = response.json()

        if response.status_code != 200:
            raise HTTPError(
                f"Encountered error while getting refresh history. Response: {response.json()}"
            )

        return raw["value"]

    def post_dataset_user(
        self,
        identifier: str,
        principal_type: str,
        dataset_user_access_right: str,
    ) -> None:
        if self.group_id:
            path = f"groups/{self.group_id}/datasets/{self.id}/users"
        else:
            path = f"datasets/{self.id}/users"

        resource = self.BASE_URL + path
        payload = {
            "identifier": identifier,
            "principalType": principal_type,
            "datasetUserAccessRight": dataset_user_access_right,
        }

        self.post(resource, self.session, payload)
