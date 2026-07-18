import requests

from pbipy.resources import Resource


class DummyResource(Resource):
    _REPR = ["id", "name"]


def test_repr_includes_class_name_and_repr_attrs():
    resource = DummyResource(id="123", session=requests.Session())
    resource.name = "My Resource"

    representation = repr(resource)

    assert representation.startswith("<DummyResource ")
    assert "id='123'" in representation
    assert "name='My Resource'" in representation


def test_str_prefers_name_over_repr():
    resource = DummyResource(id="123", session=requests.Session())
    resource.name = "My Resource"

    assert str(resource) == "My Resource"


def test_str_falls_back_to_id_when_no_name():
    resource = DummyResource(id="123", session=requests.Session())

    assert str(resource) == "123"


def test_str_falls_back_to_repr_when_no_identifying_attrs():
    resource = DummyResource.__new__(DummyResource)

    assert str(resource) == repr(resource)
