import pytest
import responses


@pytest.fixture
def admin(powerbi):
    return powerbi.admin()


@responses.activate
def test_app_users(admin, get_app_users_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/users",
        body=get_app_users_as_admin,
        content_type="application/json",
    )

    users = admin.app_users("f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)
