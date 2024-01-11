"""pbipy Resource definition."""

from requests import Session

from pbipy import settings
from pbipy import _utils


class Resource:
    """
    Represents a URL-addressable resource in the Power BI Rest API.

    Resources are Power BI components such as Apps, Reports, Groups, 
    Datasets, etc. and closely mirror the REST Operation Groups here:

    https://learn.microsoft.com/en-us/rest/api/power-bi/
    
    Resources translate the JSON returned by the API into more user-friendly 
    Python representations.

    """

    BASE_URL = settings.BASE_URL

    def __init__(
        self,
        id: str,
        session: Session,
        **kwargs,
    ) -> None:
        self.id = id
        self.session = session
        self.raw = None

    def __repr__(
        self,
    ) -> str:
        """
        Provide a readable representation of the class. Looks to the class'
        `self._REPR` to determine what to show.

        Returns
        -------
        `str`
            Formatted, readable representation of the class.
        """

        name = self.__class__.__name__

        attrs = []
        for attr in self._REPR:
            if attr in self.__dict__.keys():
                attr_str = "{}={!r}".format(attr, self.__dict__.get(attr))
                attrs.append(attr_str)

        return f"<{name} {', '.join(attrs)}>"

    def _load_from_raw(self, raw):
        self.raw = raw

        for k, v in raw.items():
            attr = _utils.to_identifier(k)
            attr = _utils.to_snake_case(attr)
            setattr(self, attr, v)

        return self

    def load(self):
        raw = _utils.get_raw(
            self.base_path,
            self.session,
        )
        self._load_from_raw(raw)
