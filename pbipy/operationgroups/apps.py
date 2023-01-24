"""Operations for working with Apps."""

from ..models import App


class Apps:
    """
    Operations for working with apps.

    Methods correspond to end points laid out at:

    https://learn.microsoft.com/en-us/rest/api/power-bi/apps

    Parameters
    ----------
    `client` : `PowerBI`
        pbipy PowerBI client for handling interactions with API.
    """

    def __init__(self, client):
        self.client = client

    def get_apps(self):
        """
        Returns a list of installed apps.

        Returns
        -------
        `list`
            List of `App` objects.
        """

        resource = "https://api.powerbi.com/v1.0/myorg/apps"

        return self.client._get_and_load_resource(resource, model=App)
