import pytest
import responses
from responses import matchers
import requests

from pbipy.groups import Group


@pytest.fixture
def group():
    raw = {
        "id": "e2284830-c8dc-416b-b19a-8cdcd2729332",
        "isReadOnly": False,
        "isOnDedicatedCapacity": False,
        "name": "sample group",
    }

    group = Group(
        raw.get("id"),
        session=requests.Session(),
        raw=raw,
    )

    return group


def test_group_creation_from_raw():
    raw = {
        "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "isReadOnly": False,
        "isOnDedicatedCapacity": False,
        "name": "sample group",
    }

    group = Group(raw.get("id"), session=requests.Session(), raw=raw)

    assert group.id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert group.is_read_only == False
    assert group.is_on_dedicated_capacity == False
    assert group.name == "sample group"


@responses.activate
def test_groups_call(powerbi, get_groups):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups",
        body=get_groups,
        content_type="application/json",
    )

    powerbi.groups()


@responses.activate
def test_group_add_user_call():
    json_params = {
        "identifier": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
        "groupUserAccessRight": "Admin",
        "principalType": "App",
        "emailAddress": "john@contoso.com",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/users",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    group.add_user(
        identifier="1f69e798-5852-4fdd-ab01-33bb14b6e934",
        principal_type="App",
        access_right="Admin",
        email_address="john@contoso.com",
    )


@responses.activate
def test_group_remove_user_call():
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/users/john@contoso.com",
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    group.delete_user("john@contoso.com")


@responses.activate
def test_group_update_user_call():
    json_params = {
        "identifier": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
        "groupUserAccessRight": "Admin",
        "principalType": "App",
        "emailAddress": "john@contoso.com",
    }

    responses.put(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/users",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    group.update_user(
        identifier="1f69e798-5852-4fdd-ab01-33bb14b6e934",
        principal_type="App",
        access_right="Admin",
        email_address="john@contoso.com",
    )


@responses.activate
def test_group_users_call(get_group_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/users",
        body=get_group_users,
        content_type="application/json",
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    group.users()


@responses.activate
def test_group_users_call_params(get_group_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/users?$top=3&$skip=1",
        body=get_group_users,
        content_type="application/json",
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    group.users(top=3, skip=1)


@responses.activate
def test_group_users_result(get_group_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/users",
        body=get_group_users,
        content_type="application/json",
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    users = group.users()

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


@responses.activate
def test_create_group_call(powerbi, create_group):
    json_params = {"name": "sample workspace"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        body=create_group,
        content_type="application/json",
    )

    powerbi.create_group("sample workspace")


@responses.activate
def test_create_group_call_with_workspacev2(powerbi, create_group):
    json_params = {"name": "sample workspace"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups?workspaceV2=True",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        body=create_group,
        content_type="application/json",
    )

    powerbi.create_group("sample workspace", workspace_v2=True)


@responses.activate
def test_create_group_result(powerbi, create_group):
    json_params = {"name": "sample workspace"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        body=create_group,
        content_type="application/json",
    )

    group = powerbi.create_group("sample workspace")

    assert isinstance(group, Group)
    assert hasattr(group, "id")
    assert hasattr(group, "name")
    assert hasattr(group, "is_on_dedicated_capacity")

    assert group.id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert not group.is_on_dedicated_capacity
    assert group.name == "sample group"


@responses.activate
def test_group_update(group):
    json_params = {
        "name": "Sample Group 1",
        "defaultDatasetStorageFormat": "Small",
    }
    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/groups/e2284830-c8dc-416b-b19a-8cdcd2729332",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    group.update(name="Sample Group 1", default_dataset_storage_format="Small")

    # Changes were made
    assert group.name == "Sample Group 1"
    assert group.default_dataset_storage_format == "Small"
    assert group.raw.get("defaultDatasetStorageFormat") == "Small"

    # Existing values unaffected
    assert group.is_read_only == False
    assert group.raw.get("isOnDedicatedCapacity") == False


@responses.activate
def test_group_update_name(group):
    json_params = {
        "name": "Sample Group 1",
    }
    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/groups/e2284830-c8dc-416b-b19a-8cdcd2729332",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    group.update(name="Sample Group 1")

    assert group.name == "Sample Group 1"
    assert group.raw.get("name") == "Sample Group 1"


@responses.activate
def test_group_update_raises(group):
    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/groups/e2284830-c8dc-416b-b19a-8cdcd2729332",
    )

    with pytest.raises(ValueError):
        group.update()
