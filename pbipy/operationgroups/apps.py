"""Operations for working with Apps."""

from ..models import App, Report


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
    
    def get_app(self, app_id):
        """
        Returns the specified installed app.

        Parameters
        ----------
        id : `str`
            Id of the App to get.
        
        Returns
        -------
        `App`
            App matching the specified Id.
        """

        # TODO: What if the App isn't found?

        resource = "https://api.powerbi.com/v1.0/myorg/apps/{0}"

        return self.client._get_and_load_resource(resource, app_id, model=App)

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

    def get_reports(self, app):
        """
        Returns a list of the reports attached to the specified app.

        Parameters
        ----------
        `app` : `Union[str, App]`
            The App Id or `App` object to retrieve the Reports for.

        Returns
        -------
        `list`
            List of `Report` objects attached to the specified app.
        """
        if isinstance(app, App):
            app_id = app.id
        else:
            app_id = app

        resource = "https://api.powerbi.com/v1.0/myorg/apps/{0}/reports"
        return self.client._get_and_load_resource(resource, app_id, model=Report)
