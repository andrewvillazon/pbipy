from requests import Session

from pbipy import settings
from pbipy.utils import RequestsMixin, to_snake_case


class Resource(RequestsMixin):
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
            attr = to_snake_case(k)
            setattr(self, attr, v)

        return self

    def load(self):
        raw = self.get_raw(self.base_path, self.session)
        self._load_from_raw(raw)


class Report(Resource):
    def __init__(
        self,
        id: str,
        session: Session,
        group_id: str = None,
        raw: dict = None,
    ) -> None:
        super().__init__(id, session)

        if group_id:
            self.group_id = group_id
        else:
            self.group_id = None

        if self.group_id:
            self.resource_path = f"/groups/{self.group_id}/reports/{self.id}"
        else:
            self.resource_path = f"/reports/{self.id}"

        self.base_path = f"{self.BASE_URL}{self.resource_path}"

        if raw:
            self._load_from_raw(raw)
    