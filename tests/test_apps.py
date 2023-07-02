import pytest
import requests

from pbipy.apps import App


@pytest.fixture
def app():
    raw = {
        "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "description": "The finance app",
        "name": "Finance",
        "publishedBy": "Bill",
        "lastUpdate": "2019-01-13T09:46:53.094+02:00",
    }

    app = App(
        id=raw["id"],
        session=requests.Session(),
        raw=raw,
    )

    return app


def test_app_creation(app):
    assert isinstance(app, App)
    assert app.id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert app.description == "The finance app"
