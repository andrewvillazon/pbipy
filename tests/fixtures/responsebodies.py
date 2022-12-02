import pytest


@pytest.fixture
def get_dataset():
    return """
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


@pytest.fixture
def get_dataset_in_group():
    return """
    {
    "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    "name": "SalesMarketing",
    "addRowsAPIEnabled": false,
    "configuredBy": "john@contoso.com",
    "isRefreshable": true,
    "isEffectiveIdentityRequired": false,
    "isEffectiveIdentityRolesRequired": false,
    "isOnPremGatewayRequired": false,
    "upstreamDatasets": []
    }
    """


@pytest.fixture
def get_datasets_in_group():
    return """
    {
    "value": [
        {
            "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "name": "SalesMarketing",
            "addRowsAPIEnabled": false,
            "configuredBy": "john@contoso.com",
            "isRefreshable": true,
            "isEffectiveIdentityRequired": false,
            "isEffectiveIdentityRolesRequired": false,
            "isOnPremGatewayRequired": false
        }
    ]
    }
    """

@pytest.fixture
def get_refresh_history():
    return """
        {
        "value": [
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "status": "Completed",
            "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
            },
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "serviceExceptionJson": "{\\"errorCode\\":\\"ModelRefreshFailed_CredentialsNotSpecified\\"}",
            "status": "Failed",
            "requestId": "11bf290a-346b-48b7-8973-c5df149337ff"
            }
        ]
        }
        """


@pytest.fixture
def get_dataset_to_dataflow_links_in_group():
    return """
        {
        "value": [
            {
            "datasetObjectId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "dataflowObjectId": "928228ba-008d-4fd9-864a-92d2752ee5ce",
            "workspaceObjectId": "f089354e-8366-4e18-aea3-4cb4a3a50b48"
            }
        ]
        }
        """


@pytest.fixture
def get_dataset_users():
    return """
        {
        "value": [
            {
            "identifier": "john@contoso.com",
            "principalType": "User",
            "datasetUserAccessRight": "Read"
            },
            {
            "identifier": "154aef10-47b8-48c4-ab97-f0bf9d5f8fcf",
            "principalType": "Group",
            "datasetUserAccessRight": "ReadReshare"
            },
            {
            "identifier": "3d9b93c6-7b6d-4801-a491-1738910904fd",
            "principalType": "App",
            "datasetUserAccessRight": "ReadWriteReshareExplore"
            }
        ]
        }
        """