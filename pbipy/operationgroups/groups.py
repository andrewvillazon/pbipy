from ..models import Group


class Groups:
    """
    Operations for working with groups.

    Methods correspond to end points laid out at:

    https://learn.microsoft.com/en-us/rest/api/power-bi/groups

    Parameters
    ----------
    `client` : `PowerBI`
        pbipy PowerBI client for handling interactions with API.
    """

    def __init__(self, client):
        self.client = client
    
    def get_groups(self, filter=None, top=None, skip=None):
        """
        Return a list of workspaces the user has access to.

        Parameters
        ----------
        `filter` : `str`
            Filters the results, based on a boolean condition, by default None
        `top` : `int`
            Returns only the first n results, by default None
        `skip` : `int`
            Skip the first n results, by default None

        Returns
        -------
        `list`
            List of `Group` objects.
        """

        resource = "https://api.powerbi.com/v1.0/myorg/groups"
        params = {
            "$filter": filter,
            "$top": top,
            "$skip": skip,
        }
        return self.client._get_and_load_resource(resource, model=Group, parameters=params)
