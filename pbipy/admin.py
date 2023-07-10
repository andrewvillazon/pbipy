import requests

from pbipy import settings
from pbipy.apps import App
from pbipy.utils import RequestsMixin


class Admin(RequestsMixin):
    BASE_URL = settings.BASE_URL

    def __init__(
        self,
        session: requests.Session,
    ) -> None:
        self.session = session

        self.resource_path = "/admin"
        self.base_path = f"{self.BASE_URL}{self.resource_path}"

    def apps(
        self,
        top: int = None,
    ) -> list[App]:
        """
        Return a list of Apps in the Organization.

        Parameters
        ----------
        top : `int`, optional
            The requested number of entries in the refresh history. If not
            provided, the default is all available entries.

        Returns
        -------
        `list[App]`
            The list of Apps for the organization.

        """

        resource = self.base_path + "/apps"
        params = {"$top": top}

        raw = self.get_raw(resource, self.session, params)

        apps = [
            App(
                app_js.get("id"),
                self.session,
                raw=app_js,
            )
            for app_js in raw
        ]

        return apps

    def app_users(
        self,
        app: str | App,
    ) -> list[dict]:
        if isinstance(app, App):
            app_id = app.id
        else:
            app_id = app

        resource = self.base_path + f"/apps/{app_id}/users"
        raw = self.get_raw(resource, self.session)

        return raw
