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


@pytest.fixture
def get_parameters():
    return """
    {
      "value": [
        {
          "name": "ServerName",
          "type": "Text",
          "isRequired": true,
          "currentValue": "MyTest.database.windows.net"
        },
        {
          "name": "DatabaseName",
          "type": "Text",
          "isRequired": true,
          "currentValue": "MyTestDB"
        },
        {
          "name": "FromDate",
          "type": "DateTime",
          "isRequired": true,
          "currentValue": "2/8/2002 12:00:00 AM"
        },
        {
          "name": "FilterBlanks",
          "type": "Logical",
          "isRequired": true,
          "currentValue": "TRUE"
        },
        {
          "name": "MaxId",
          "type": "Number",
          "isRequired": true,
          "currentValue": "77"
        },
        {
          "name": "AnyParam",
          "type": "Any",
          "isRequired": true,
          "currentValue": "uu63"
        }
      ]
    }
    """


@pytest.fixture
def get_refresh_execution_details():
    return """
    {
      "startTime": "2021-12-10T08:40:31.57",
      "endTime": "2021-12-10T08:40:43.87",
      "type": "Full",
      "commitMode": "Transactional",
      "status": "Completed",
      "extendedStatus": "Completed",
      "currentRefreshType": "Full",
      "numberOfAttempts": 0,
      "objects": [
        {
          "table": "DateTableTemplate_78e78207-b3fb-41b5-8b95-e5efca989067",
          "partition": "DateTableTemplate_78e78207-b3fb-41b5-8b95-e5efca989067-ae306fb4-3b7e-4a41-824d-cb3b452fedfc",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_e9d8a66b-4018-4d16-be8c-402b2037c051",
          "partition": "LocalDateTable_e9d8a66b-4018-4d16-be8c-402b2037c051-59bc07f8-85c9-456a-ad36-18e1de4d77ed",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_55935f6b-04d1-4cfe-8856-ed9f9e73ab2e",
          "partition": "LocalDateTable_55935f6b-04d1-4cfe-8856-ed9f9e73ab2e-d95ae7f7-19c9-48a8-9c16-fcab26558bc2",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_ff25f80e-eb04-4229-986d-b40223c04f1c",
          "partition": "LocalDateTable_ff25f80e-eb04-4229-986d-b40223c04f1c-6606fc4c-4cda-49e1-8acd-e55a6ec36cb3",
          "status": "Completed"
        },
        {
          "table": "DimCurrency",
          "partition": "DimCurrency-e5524cc4-a898-433b-91aa-c001b9a6d676",
          "status": "Completed"
        },
        {
          "table": "DimCustomer",
          "partition": "DimCustomer-a31bbd93-e20a-4dee-a33c-7afa27785953",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_fa65a206-f320-4d5d-abcc-1dc0f051ca7d",
          "partition": "LocalDateTable_fa65a206-f320-4d5d-abcc-1dc0f051ca7d-06a48a0a-a32b-48a3-b113-924aafd6363c",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_78a4e1b7-a2e5-4bbf-ab68-7c87961b68a2",
          "partition": "LocalDateTable_78a4e1b7-a2e5-4bbf-ab68-7c87961b68a2-5b3ba715-7c84-4e52-b310-485b93cfbe6d",
          "status": "Completed"
        },
        {
          "table": "DimDate",
          "partition": "DimDate-62e2f91b-53e5-4ed3-8618-fec74dba5e0d",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_e72c294f-0a06-4051-b943-e6bf8389e2c3",
          "partition": "LocalDateTable_e72c294f-0a06-4051-b943-e6bf8389e2c3-891a0e68-d414-4ba3-9c4b-e6f1ec73d4f3",
          "status": "Completed"
        },
        {
          "table": "DimProduct",
          "partition": "DimProduct-3d07cc89-2bd7-4a98-bb37-3368c1562f98",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_e37e4431-8c1a-449c-8796-b704df200a92",
          "partition": "LocalDateTable_e37e4431-8c1a-449c-8796-b704df200a92-8596ebb8-418f-4e50-a921-dac88c6f1339",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_73faffeb-a0c7-4ea1-83dc-530823b0fea0",
          "partition": "LocalDateTable_73faffeb-a0c7-4ea1-83dc-530823b0fea0-13795c4e-708f-4ddc-8ea3-5a2f39ae2253",
          "status": "Completed"
        },
        {
          "table": "DimPromotion",
          "partition": "DimPromotion-21e6c333-430e-4350-8c94-cdceb362c4c7",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_9c19746b-db7d-4b7e-b95d-c66e4b8fefc8",
          "partition": "LocalDateTable_9c19746b-db7d-4b7e-b95d-c66e4b8fefc8-395de144-ad53-41c0-9ec0-68bab6158d99",
          "status": "Completed"
        },
        {
          "table": "LocalDateTable_d96435dd-6110-4246-996c-616c96125e71",
          "partition": "LocalDateTable_d96435dd-6110-4246-996c-616c96125e71-891737ee-c46c-4b9f-bfa8-e4555004e20f",
          "status": "Completed"
        },
        {
          "table": "DimSalesTerritory",
          "partition": "DimSalesTerritory-6d88f938-13d5-49f8-899c-d11b3d346ad5",
          "status": "Completed"
        },
        {
          "table": "FactInternetSales",
          "status": "Completed"
        }
      ]
    }
    """


@pytest.fixture
def get_groups():
    return """
    {
      "value": [
        {
          "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
          "isReadOnly": false,
          "isOnDedicatedCapacity": false,
          "name": "sample group"
        },
        {
          "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "isReadOnly": false,
          "isOnDedicatedCapacity": false,
          "name": "marketing group"
        },
        {
          "id": "a2f89923-421a-464e-bf4c-25eab39bb09f",
          "isReadOnly": false,
          "isOnDedicatedCapacity": false,
          "name": "contoso",
          "dataflowStorageId": "d692ae06-708c-485e-9987-06ff0fbdbb1f"
        }
      ]
    }
    """
