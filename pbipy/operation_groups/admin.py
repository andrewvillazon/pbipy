"""Operations for working with administrative tasks."""

class Admin:
    """
    Operations for working with administrative tasks.

    Methods correspond to end points laid out at:

    https://learn.microsoft.com/en-us/rest/api/power-bi/admin

    Parameters
    ----------
    `client` : `PowerBI`
        pbipy PowerBI client for handling interactions with API.
    """

    def __init__(self, client):
        self.client = client
    
    def get_activity_events(self, start_date_time, end_date_time, filter=None):
        """
        Returns a list of Activity Events on the Power BI Instance for a
        given time period. Activity Events can include viewing reports,
        downloading reports, modifying datasets, etc.

        Note: Due to a limitation of the Power BI Rest API, the start and
        end date times must be for the same UTC day. In other words, this
        method can only query the API one day at a time.

        If the number of Activity Events exceeds the API's limit, then this
        method will continue to call the API until all records are retrieved.

        Parameters
        ----------
        `start_date_time` : `str`
            Start date and time of the time period for audit event results.
            Must be in ISO 8601 compliant UTC format: 'yyyy-mm-ddThh:mm:ss.SSSZ'
        `end_date_time` : `str`
            End date and time of the time period for audit event results. Must
            be in ISO 8601 compliant UTC format: 'yyyy-mm-ddThh:mm:ss.SSSZ'
        `filter` : `str`
            Filters the results based on a boolean condition, using 'Activity',
            'UserId', or both properties. Supports only 'eq' and 'and' operators.

        Returns
        -------
        `list`
            List of `ActivityEvent` objects.

        Raises
        ------
        `ValueError`
            If supplied start and end times are invalid.
        """

        # TODO: Add support for passing in datetime types
        # TODO: Implment logging. Especially if this is making continuous calls.

        resource = "https://api.powerbi.com/v1.0/myorg/admin/activityevents"
        params = {
            # API expects dtms to be enclosed in single quotes.
            "startDateTime": "'" + start_date_time + "'",
            "endDateTime": "'" + end_date_time + "'",
            "$filter": filter,
        }

        raw = self.client._get_resource(resource, parameters=params)

        # Handle json errors
        if "error" in raw:
            error = raw["error"]
            message = error["message"]

            if "within the same UTC day" in message:
                raise ValueError(
                    "start_date_time and end_date_time must be on the same UTC day."
                )

        # API will return continuation token when further requests needed to
        # get all data. "continuationToken" will be null when no more data.

        activity_events = raw["activityEventEntities"]
        continuation_token = raw["continuationToken"]
        continuation_uri = raw["continuationUri"]

        while continuation_token:
            raw = self.client._get_resource(continuation_uri)
            activity_events.extend(raw["activityEventEntities"])
            continuation_token = raw["continuationToken"]
            continuation_uri = raw["continuationUri"]

        return activity_events
