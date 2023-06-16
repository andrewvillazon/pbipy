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
def get_datasets():
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
        },
        {
          "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
          "name": "MarketingSales",
          "addRowsAPIEnabled": true,
          "configuredBy": "john@contoso.com",
          "isRefreshable": false,
          "isEffectiveIdentityRequired": false,
          "isEffectiveIdentityRolesRequired": false,
          "isOnPremGatewayRequired": false
        }
      ]
    }
    """


@pytest.fixture
def execute_queries():
    return """
    {
      "results": [
        {
          "tables": [
            {
              "rows": [
                {
                  "MyTable[Year]": 2010,
                  "MyTable[Quarter]": "Q1"
                },
                {
                  "MyTable[Year]": 2010,
                  "MyTable[Quarter]": "Q2"
                },
                {
                  "MyTable[Year]": 2011,
                  "MyTable[Quarter]": "Q1"
                }
              ]
            }
          ]
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


@pytest.fixture
def get_datasources():
    return """
    {
      "value": [
        {
          "datasourceType": "AzureBlobs",
          "datasourceId": "e0315274-90b6-4fc0-abf2-2d60d448cb04",
          "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
          "connectionDetails": {
            "account": "myAccount",
            "domain": "blob.core.windows.net"
          }
        },
        {
          "datasourceType": "File",
          "connectionDetails": {
            "path": "c:\\\\users\\\\username\\\\documents\\\\orders1.xlsx"
          },
          "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
          "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
        },
        {
          "datasourceType": "Exchange",
          "datasourceId": "4d126fc8-1568-46aa-ba16-ccf19b18f012",
          "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
          "connectionDetails": {
            "emailAddress": "john@contoso.com"
          }
        }
      ]
    }
    """

@pytest.fixture
def get_refresh_schedule():
    return """
    {
      "days": [
        "Sunday",
        "Friday",
        "Saturday"
      ],
      "times": [
        "05:00",
        "11:30",
        "17:30",
        "23:00"
      ],
      "enabled": true,
      "localTimeZoneId": "UTC",
      "notifyOption": "MailOnFailure"
    }
    """

@pytest.fixture
def get_direct_query_refresh_schedule():
    return """
    {
      "frequency": 15,
      "days": [],
      "times": [],
      "localTimeZoneId": "UTC"
    }
    """