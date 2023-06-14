from pbipy.utils import to_snake_case


class Resource:
    BASE_URL = "https://api.powerbi.com/v1.0/myorg/"

    def __init__(self, path, session, **kwargs) -> None:
        self.path = path
        self.url = self.BASE_URL + self.path
        self.session = session
        self.js = None

        if "group_id" in kwargs:
            # If None is not part of workspace, set to "me"
            # as per pbi urls: /groups/me/etc.
            if kwargs.get("group_id") is None:
                group_id = "me"
            else:
                group_id = kwargs.get("group_id")

            setattr(self, "group_id", group_id)

    def load_from_js(self, js):
        self.js = js

        for k, v in js.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)

        return self

    def load(self):
        response = self.session.get(self.url)
        js = response.json()

        self.load_from_js(js)


class Dataset(Resource):
    def __init__(self, id, session, group_id=None) -> None:
        if group_id:
            path = f"groups/{group_id}/datasets/{id}"
        else:
            path = f"datasets/{id}"

        super().__init__(path, session, group_id=group_id)
