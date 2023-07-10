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

        self.base_path = f"{self.BASE_URL}{self.resource_path}"

    def app_users(
        self,
        app: str | App,
    ) -> list[dict]:
        if isinstance(app, App):
            app_id = app.id
        else:
            app_id = app

        resource =self.base_path + f"/apps/{app_id}/users"
        raw = self.get_raw(resource, self.session)

        return raw
