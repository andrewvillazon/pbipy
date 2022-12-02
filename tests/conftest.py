import json

import pytest

from pbipy.models import Dataset, Group, Refresh
from pbipy.powerbi import PowerBI

from .fixtures.responsebodies import *


@pytest.fixture
def powerbi():
    return PowerBI("ABC123")


@pytest.fixture
def refresh_from_raw():
    raw = {
        "refreshType": "ViaApi",
        "startTime": "2017-06-13T09:25:43.153Z",
        "endTime": "2017-06-13T09:31:43.153Z",
        "serviceExceptionJson": '{"errorCode":"ModelRefreshFailed_CredentialsNotSpecified"}',
        "status": "Failed",
        "requestId": "11bf290a-346b-48b7-8973-c5df149337ff",
    }

    return Refresh.from_raw(raw=raw)


@pytest.fixture
def group_from_raw():
    raw = {
        "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "isReadOnly": False,
        "isOnDedicatedCapacity": False,
        "name": "marketing group",
    }

    return Group.from_raw(raw=raw)


@pytest.fixture
def dataset_from_raw():
    raw = {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": False,
        "configuredBy": "john@contoso.com",
        "isRefreshable": True,
        "isEffectiveIdentityRequired": True,
        "isEffectiveIdentityRolesRequired": True,
        "isOnPremGatewayRequired": False,
        "createdDate": "2017-06-13T09:25:43.153Z",
    }

    return Dataset.from_raw(raw=raw)


@pytest.fixture
def group():
    return Group(id="3d9b93c6-7b6d-4801-a491-1738910904fd", name="marketing group")


@pytest.fixture
def dataset():
    js = json.loads(
        """
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": true,
        "isEffectiveIdentityRequired": true,
        "isEffectiveIdentityRolesRequired": true,
        "isOnPremGatewayRequired": false
        }
        """
    )
    return Dataset.from_raw(js)


@pytest.fixture
def dataset_not_refreshable():
    js = json.loads(
        """
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": false,
        "isEffectiveIdentityRequired": true,
        "isEffectiveIdentityRolesRequired": true,
        "isOnPremGatewayRequired": false
        }
        """
    )
    return Dataset.from_raw(js)
