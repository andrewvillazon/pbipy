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
def get_refresh_execution_details_failed():
    return """
    {
      "startTime": "2021-12-10T08:40:31.57",
      "endTime": "2021-12-10T08:40:43.87",
      "type": "Full",
      "commitMode": "Transactional",
      "status": "Failed",
      "extendedStatus": "Failed"
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


# Modified version of get_groups(). API doesn't actually have a
# get_group endpoint.
@pytest.fixture
def get_group():
    return """
    {
      "value": [
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


@pytest.fixture
def get_group_users():
    return """
    {
      "value": [
        {
          "displayName": "John Nick",
          "emailAddress": "john@contoso.com",
          "groupUserAccessRight": "Admin",
          "identifier": "john@contoso.com",
          "principalType": "User"
        },
        {
          "displayName": "Adam Wood",
          "emailAddress": "Adam@contoso.com",
          "groupUserAccessRight": "Member",
          "identifier": "Adam@contoso.com",
          "principalType": "User"
        },
        {
          "displayName": "ContosoTestApp",
          "groupUserAccessRight": "Admin",
          "identifier": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "principalType": "App"
        }
      ]
    }
    """


@pytest.fixture
def create_group():
    return """
        {
          "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
          "isReadOnly": false,
          "isOnDedicatedCapacity": false,
          "name": "sample group"
        }
    """


@pytest.fixture
def get_report():
    return """
    {
      "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
      "id": "5b218778-e7a5-4d73-8187-f10824047715",
      "name": "SalesMarketing",
      "webUrl": "https://app.powerbi.com//reports/5b218778-e7a5-4d73-8187-f10824047715",
      "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715"
    }
    """


@pytest.fixture
def get_datasources_in_group():
    return """
    {
      "value": [
        {
          "datasourceType": "AnalysisServices",
          "datasourceId": "f8c56590-43cb-43bf-8daa-233ba2520f55",
          "gatewayId": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
          "connectionDetails": {
            "server": "My-As-Server",
            "database": "My-As-Database"
          }
        }
      ]
    }
    """


@pytest.fixture
def get_page():
    return """
    {
      "displayName": "Regional Sales Analysis",
      "name": "ReportSection",
      "order": "0"
    }
    """


@pytest.fixture
def get_pages():
    return """
    {
      "value": [
        {
          "displayName": "Regional Sales Analysis",
          "name": "ReportSection",
          "order": "0"
        },
        {
          "displayName": "Geographic Analysis",
          "name": "ReportSection1",
          "order": "1"
        }
      ]
    }
    """


@pytest.fixture
def get_reports_in_group():
    return """
    {
      "value": [
        {
          "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
          "id": "5b218778-e7a5-4d73-8187-f10824047715",
          "name": "SalesMarketing",
          "webUrl": "https://app.powerbi.com//reports/5b218778-e7a5-4d73-8187-f10824047715",
          "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715"
        },
        {
          "datasetId": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
          "id": "8e4d5880-81d6-4804-ab97-054665050799",
          "name": "MarketingSales",
          "webUrl": "https://app.powerbi.com//reports/8e4d5880-81d6-4804-ab97-054665050799",
          "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=8e4d5880-81d6-4804-ab97-054665050799"
        }
      ]
    }
    """


@pytest.fixture
def export_to_file():
    return """
    {
      "id": "Mi9C5419i....PS4=",
      "createdDateTime": "2021-12-08T10:26:09.3069086Z",
      "lastActionDateTime": "2021-12-08T10:26:38.016851Z",
      "reportId": "cad51cfa-e740-324f-acbb-8ca43c40a2d4",
      "reportName": "Report name",
      "status": "Running",
      "percentComplete": 70,
      "resourceLocation": "...Mi9C5419i....PS4=/file",
      "resourceFileExtension": ".pptx",
      "expirationTime": "2021-12-09T10:26:11.586756Z"
    }
    """


@pytest.fixture
def get_export_to_file_status():
    return """
    {
      "id": "Mi9C5419i....PS4=",
      "createdDateTime": "2021-12-08T10:26:09.3069086Z",
      "lastActionDateTime": "2021-12-08T10:26:38.016851Z",
      "reportId": "cad51cfa-e740-324f-acbb-8ca43c40a2d4",
      "reportName": "Report name",
      "status": "Succeeded",
      "percentComplete": 100,
      "resourceLocation": "...Mi9C5419i....PS4=/file",
      "resourceFileExtension": ".pptx",
      "expirationTime": "2021-12-09T10:26:11.586756Z"
    }
    """


@pytest.fixture
def get_app():
    return """
    {
      "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
      "description": "The finance app",
      "name": "Finance",
      "publishedBy": "Bill",
      "lastUpdate": "2019-01-13T09:46:53.094+02:00"
    }
    """


@pytest.fixture
def get_apps():
    return """
    {
      "value": [
        {
          "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
          "description": "The finance app",
          "name": "Finance",
          "publishedBy": "Bill",
          "lastUpdate": "2019-01-13T09:46:53.094+02:00"
        },
        {
          "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "description": "The marketing app",
          "name": "Marketing",
          "publishedBy": "Ben",
          "lastUpdate": "2018-11-13T09:46:53.094+02:00"
        }
      ]
    }
    """


@pytest.fixture
def app_get_report():
    return """
    {
      "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
      "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
      "id": "66b2570c-d9d3-40b2-83d9-1095c6700041",
      "name": "SalesMarketing",
      "webUrl": "https://app.powerbi.com/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
      "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=66b2570c-d9d3-40b2-83d9-1095c6700041&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ"
    }
    """


@pytest.fixture
def app_get_reports():
    return """
    {
      "value": [
        {
          "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
          "id": "66b2570c-d9d3-40b2-83d9-1095c6700041",
          "name": "SalesMarketing",
          "webUrl": "https://app.powerbi.com/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
          "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=66b2570c-d9d3-40b2-83d9-1095c6700041&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ"
        }
      ]
    }
    """


@pytest.fixture
def app_get_dashboard():
    return """
    {
      "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
      "id": "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac",
      "displayName": "SalesMarketing",
      "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=335aee4b-7b38-48fd-9e2f-306c3fd67482&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ%3d%3d",
      "isReadOnly": false
    }
    """


@pytest.fixture
def app_get_dashboards():
    return """
    {
      "value": [
        {
          "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "id": "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac",
          "displayName": "SalesMarketing",
          "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=335aee4b-7b38-48fd-9e2f-306c3fd67482&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ%3d%3d",
          "isReadOnly": false
        }
      ]
    }
    """


@pytest.fixture
def app_get_tile():
    return """
    {
      "id": "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
      "title": "SalesMarketingTile",
      "embedUrl": "https://app.powerbi.com/embed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&tileId=312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48",
      "rowSpan": 0,
      "colSpan": 0,
      "reportId": "5b218778-e7a5-4d73-8187-f10824047715",
      "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    }
    """


@pytest.fixture
def app_get_tiles():
    return """
    {
      "value": [
        {
          "id": "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
          "title": "SalesMarketingTile",
          "embedUrl": "https://app.powerbi.com/embed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&tileId=312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ%3d%3d",
          "rowSpan": 0,
          "colSpan": 0,
          "reportId": "5b218778-e7a5-4d73-8187-f10824047715",
          "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
        }
      ]
    }
    """


@pytest.fixture
def get_dataflow():
    return """
    {
      "objectId": "bd32e5c0-363f-430b-a03b-5535a4804b9b",
      "name": "AdventureWorks",
      "description": "Our Adventure Works",
      "modelUrl": "https://MyDataflowStorageAccount.dfs.core.windows.net/powerbi/contoso/AdventureWorks/model.json",
      "ppdf:outputFileFormat": "csv"
    }
  """


@pytest.fixture
def get_dataflows():
    return """
    {
      "value": [
        {
          "objectId": "bd32e5c0-363f-430b-a03b-5535a4804b9b",
          "name": "AdventureWorks",
          "description": "Our Adventure Works",
          "modelUrl": "https://MyDataflowStorageAccount.dfs.core.windows.net/powerbi/contoso/AdventureWorks/model.json"
        }
      ]
    }
  """


@pytest.fixture
def get_dataflow_datasources():
    return """
    {
      "value": [
        {
          "datasourceType": "Sql",
          "datasourceId": "16a54ccd-620d-4af3-9197-0b8c779a9a6d",
          "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
          "connectionDetails": {
            "server": "MyServer.database.windows.net",
            "database": "MyDatabase"
          }
        },
        {
          "datasourceType": "OData",
          "connectionDetails": {
            "url": "https://services.odata.org/V4/Northwind/Northwind.svc"
          },
          "datasourceId": "16a54ccd-620d-4af3-9197-0b8c779a9a6d",
          "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674"
        }
      ]
    }
  """


@pytest.fixture
def get_dataflow_transactions():
    return """
    {
      "@odata.context": "http://someserver.analysis.windows.net/v1.0/myorg/groups/98674fdf-baab-45e1-a04a-c17ab378dce1/$metadata#transactions",
      "value": [
        {
          "id": "2020-08-27T16:07:47.2487692Z@8dbd8c92-4d16-4947-8329-4172f04f4f93$2"
        },
        {
          "id": "2020-08-26T16:40:55.0968787Z@e33eed4d-5b1a-4bb9-8b5b-dff1cd371109$1",
          "refreshType": "OnDemand"
        }
      ]
    }
  """


@pytest.fixture
def cancel_dataflow_transaction():
    return """
    {
      "transactionId": "2020-09-11T19:21:52.8778432Z@9cc7a369-6112-4dba-97b6-b07ff5699568$1374282",
      "status": "SuccessfullyMarked"
    }
"""


@pytest.fixture
def get_app_users_as_admin():
    return """
    {
      "value": [
        {
          "displayName": "John Nick",
          "emailAddress": "john@contoso.com",
          "appUserAccessRight": "ReadExplore",
          "identifier": "john@contoso.com",
          "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
          "principalType": "User"
        }
      ]
    }
    """


@pytest.fixture
def get_apps_as_admin():
    return """
    {
      "value": [
        {
          "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
          "description": "The finance app",
          "name": "Finance",
          "publishedBy": "Bill",
          "lastUpdate": "2019-01-13T09:46:53.094+02:00"
        },
        {
          "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "description": "The marketing app",
          "name": "Marketing",
          "publishedBy": "Ben",
          "lastUpdate": "2018-11-13T09:46:53.094+02:00"
        }
      ]
    }
    """


@pytest.fixture
def get_dashboards_as_admin():
    return """
    {
      "value": [
        {
          "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
          "displayName": "SalesMarketing",
          "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
          "isReadOnly": false,
          "workspaceId": "abfbdc89-2659-43c1-9142-93e8378eac96"
        }
      ]
    }
    """


@pytest.fixture
def get_dataflow_datasources_as_admin():
    return """
    {
      "value": [
        {
          "name": "301",
          "connectionString": "data source=MyServer.database.windows.net;initial catalog=MyDatabase;persist security info=True;encrypt=True;trustservercertificate=False",
          "datasourceType": "Sql",
          "datasourceId": "16a54ccd-620d-4af3-9197-0b8c779a9a6d",
          "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
          "connectionDetails": {
            "server": "MyServer.database.windows.net",
            "database": "MyDatabase"
          }
        }
      ]
    }
    """


@pytest.fixture
def get_dataflow_users_as_admin():
    return """
    {
      "value": [
        {
          "displayName": "John Nick",
          "emailAddress": "john@contoso.com",
          "dataflowUserAccessRight": "ReadWrite",
          "identifier": "john@contoso.com",
          "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
          "principalType": "User"
        }
      ]
    }
    """


@pytest.fixture
def get_upstream_dataflows_in_group_as_admin():
    return """
    {
      "value": [
        {
          "targetDataflowId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
          "groupId": "f089354e-8366-4e18-aea3-4cb4a3a50b48"
        },
        {
          "targetDataflowId": "67a4529b-0cdd-4584-9867-5c0e77d57a2f",
          "groupId": "f089354e-8366-4e18-aea3-4cb4a3a50b48"
        }
      ]
    }
    """


@pytest.fixture
def get_dataset_to_dataflow_links_in_group_as_admin():
    return """
    {
      "value": [
        {
          "datasetObjectId": "0d6e2a35-c606-4fb7-8690-1b3a5370a294",
          "dataflowObjectId": "4caab73a-2660-4255-8e53-de6745f3d92c",
          "workspaceObjectId": "358240c2-b8f3-4817-aa7a-0efa03687a7b"
        }
      ]
    }
    """


@pytest.fixture
def get_dataset_users_as_admin():
    return """
    {
      "value": [
        {
          "displayName": "John Nick",
          "emailAddress": "john@contoso.com",
          "datasetUserAccessRight": "ReadWriteReshareExplore",
          "identifier": "john@contoso.com",
          "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
          "principalType": "User"
        }
      ]
    }
    """


@pytest.fixture
def get_datasets_as_admin():
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
          "isOnPremGatewayRequired": false,
          "isInPlaceSharingEnabled": false,
          "workspaceId": "5c968528-70b6-4588-809f-ce811ffa5c23"
        }
      ]
    }
    """


@pytest.fixture
def get_datasets_in_group_as_admin():
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
          "isOnPremGatewayRequired": false,
          "isInPlaceSharingEnabled": false
        }
      ]
    }
    """


@pytest.fixture
def get_dataflows_as_admin():
    return """
    {
      "value": [
        {
          "objectId": "bd32e5c0-363f-430b-a03b-5535a4804b9b",
          "name": "AdventureWorks",
          "description": "Our Adventure Works",
          "modelUrl": "https://MyDataflowStorageAccount.dfs.core.windows.net/powerbi/contoso/AdventureWorks/model.json",
          "configuredBy": "john@contoso.com",
          "workspaceId": "6369a442-4bc4-425c-916d-460c42be746b"
        }
      ]
    }
    """


@pytest.fixture
def get_dataflows_in_group_as_admin():
    return """
    {
      "value": [
        {
          "objectId": "bd32e5c0-363f-430b-a03b-5535a4804b9b",
          "name": "AdventureWorks",
          "description": "Our Adventure Works",
          "modelUrl": "https://MyDataflowStorageAccount.dfs.core.windows.net/powerbi/contoso/AdventureWorks/model.json",
          "configuredBy": "john@contoso.com"
        }
      ]
    }
    """


@pytest.fixture
def add_power_bi_encryption_key():
    return """
    {
      "id": "82d9a37a-2b45-4221-b012-cb109b8e30c7",
      "name": "Contoso Sales",
      "keyVaultKeyIdentifier": "https://contoso-vault2.vault.azure.net/keys/ContosoKeyVault/b2ab4ba1c7b341eea5ecaaa2wb54c4d2",
      "isDefault": true,
      "createdAt": "2019-04-30T21:35:15.867-07:00",
      "updatedAt": "2019-04-30T21:35:15.867-07:00"
    }
    """


@pytest.fixture
def get_dashboard_subscriptions_as_admin():
    return """
    {
      "value": [
        {
          "id": "18b746fe-c6d5-4a00-9523-05dc91424275",
          "title": "TestDashboardSubscription-1",
          "artifactId": "7b71b90a-a333-4006-b12c-ef3d767fa4e9",
          "artifactDisplayName": "Customer Profitability Sample",
          "artifactType": "Dashboard",
          "isEnabled": true,
          "frequency": "Daily",
          "startDate": "10/13/2021 12:00:00 AM",
          "endDate": "10/13/2022 12:00:00 AM",
          "linkToContent": true,
          "previewImage": false,
          "users": [
            {
              "displayName": "John Nick",
              "emailAddress": "john@contoso.com",
              "identifier": "john@contoso.com",
              "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
              "principalType": "User"
            }
          ]
        }
      ]
    }
    """


@pytest.fixture
def get_dashboard_users_as_admin():
    return """
    {
      "value": [
        {
          "displayName": "John Nick",
          "emailAddress": "john@contoso.com",
          "dashboardUserAccessRight": "Owner",
          "identifier": "john@contoso.com",
          "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
          "principalType": "User"
        }
      ]
    }
    """


@pytest.fixture
def get_tiles_as_admin():
    return """
    {
      "value": [
        {
          "id": "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
          "title": "SalesMarketingTile",
          "embedUrl": "https://app.powerbi.com/embed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&tileId=312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
          "rowSpan": 0,
          "colSpan": 0,
          "reportId": "5b218778-e7a5-4d73-8187-f10824047715",
          "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
        }
      ]
    }
    """


@pytest.fixture
def get_datasources_as_admin():
    return """
    {
      "value": [
        {
          "name": "301",
          "connectionString": "data source=MyServer.database.windows.net;initial catalog=MyDatabase;persist security info=True;encrypt=True;trustservercertificate=False",
          "datasourceType": "Sql",
          "datasourceId": "16a54ccd-620d-4af3-9197-0b8c779a9a6d",
          "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
          "connectionDetails": {
            "server": "MyServer.database.windows.net",
            "database": "MyDatabase"
          }
        }
      ]
    }
    """


@pytest.fixture
def get_power_bi_encryption_keys():
    return """
    {
      "value": [
        {
          "id": "82d9a37a-2b45-4221-b012-cb109b8e30c7",
          "name": "Contoso Sales",
          "keyVaultKeyIdentifier": "https://contoso-vault2.vault.azure.net/keys/ContosoKeyVault/b2ab4ba1c7b341eea5ecaaa2wb54c4d2",
          "isDefault": true,
          "createdAt": "2019-04-30T21:35:15.867-07:00",
          "updatedAt": "2019-04-30T21:35:15.867-07:00"
        }
      ]
    }
    """


@pytest.fixture
def get_groups_as_admin():
    return """
    {
      "value": [
        {
          "id": "183dcf10-47b8-48c4-84aa-f0bf9d5f8fcf",
          "isReadOnly": false,
          "isOnDedicatedCapacity": false,
          "name": "Sample Group 2",
          "description": "Deleted sample group",
          "type": "Workspace",
          "state": "Deleted"
        }
      ]
    }
    """


@pytest.fixture
def get_groups_as_admin_with_expand():
    return """
    {
      "value": [
        {
          "id": "94E57E92-CEE2-486D-8CC8-218C97200579",
          "isReadOnly": false,
          "isOnDedicatedCapacity": false,
          "capacityMigrationStatus": "Migrated",
          "description": "shorter description",
          "type": "Workspace",
          "state": "Removing",
          "name": "a",
          "hasWorkspaceLevelSettings": false,
          "dashboards": [
            {
              "id": "4668133c-ae3f-42fb-ad7c-214a8623280c",
              "displayName": "SQlAzure-Refresh.pbix",
              "isReadOnly": false
            },
            {
              "id": "a8f18ca7-63e8-4220-bc1c-f576ec180b98",
              "displayName": "cdvc",
              "isReadOnly": false
            }
          ]
        }
      ]
    }
    """


@pytest.fixture
def get_group_users_as_admin():
    return """
    {
      "value": [
        {
          "displayName": "John Nick",
          "emailAddress": "john@contoso.com",
          "groupUserAccessRight": "Admin",
          "identifier": "john@contoso.com",
          "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
          "principalType": "User"
        },
        {
          "displayName": "Adam Wood",
          "emailAddress": "Adam@contoso.com",
          "groupUserAccessRight": "Member",
          "identifier": "Adam@contoso.com",
          "graphId": "785e192c-0f1f-41ca-ae7a-a85da28e565a",
          "principalType": "User"
        },
        {
          "displayName": "ContosoTestApp",
          "groupUserAccessRight": "Admin",
          "identifier": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "graphId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
          "principalType": "App"
        }
      ]
    }
"""


@pytest.fixture
def get_report_subscriptions_as_admin():
    return """
    {
      "value": [
        {
          "id": "18b746fe-c6d5-4a00-9523-05dc91424274",
          "title": "TestReportSubscription-1",
          "artifactId": "7b71b90a-a333-4006-b12c-ef3d767fa4e9",
          "artifactDisplayName": "Customer Profitability Sample",
          "subArtifactDisplayName": "Team Scorecard",
          "artifactType": "Report",
          "isEnabled": true,
          "frequency": "Daily",
          "startDate": "10/13/2021 12:00:00 AM",
          "endDate": "10/13/2022 12:00:00 AM",
          "linkToContent": true,
          "previewImage": true,
          "attachmentFormat": "PNG",
          "users": [
            {
              "displayName": "John Nick",
              "emailAddress": "john@contoso.com",
              "identifier": "john@contoso.com",
              "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
              "principalType": "User"
            }
          ]
        }
      ]
    }
    """


@pytest.fixture
def get_report_users_as_admin():
    return """
    {
      "value": [
        {
          "displayName": "John Nick",
          "emailAddress": "john@contoso.com",
          "reportUserAccessRight": "Owner",
          "identifier": "john@contoso.com",
          "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
          "principalType": "User"
        }
      ]
    }
    """


@pytest.fixture
def get_reports_as_admin():
    return """
    {
      "value": [
        {
          "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
          "id": "5b218778-e7a5-4d73-8187-f10824047715",
          "name": "SalesMarketing",
          "webUrl": "https://app.powerbi.com//reports/5b218778-e7a5-4d73-8187-f10824047715",
          "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715",
          "workspaceId": "278e22a3-2aee-4057-886d-c3225423bc10"
        }
      ]
    }
    """


@pytest.fixture
def get_reports_in_group_as_admin():
    return """
    {
      "value": [
        {
          "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
          "id": "5b218778-e7a5-4d73-8187-f10824047715",
          "name": "SalesMarketing",
          "webUrl": "https://app.powerbi.com/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/5b218778-e7a5-4d73-8187-f10824047715",
          "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48"
        }
      ]
    }
    """


@pytest.fixture
def get_activity_events():
    return [
        """
        {
          "activityEventEntities": [
            {
              "Id": "41ce06d1-d81b-4ea0-bc6d-2ce3dd2f8e87",
              "CreationTime": "2019-08-13T07:55:15",
              "Operation": "ViewReport",
              "OrganizationId": "e43e3248-3d83-44aa-a94d-c836bd7f9b79",
              "UserKey": "123456",
              "Activity": "ViewReport",
              "Workload": "PowerBI",
              "UserId": "john@contoso.com",
              "ClientIP": "127.0.0.1"
            },
            {
              "Id": "c632aa64-70fc-4e80-88f3-9fc2cdcacce8",
              "CreationTime": "2019-08-13T07:55:10",
              "Operation": "ViewReport",
              "OrganizationId": "e43e3248-3d83-44aa-a94d-c836bd7f9b79",
              "UserKey": "42343KJK53K45J",
              "Activity": "ViewReport",
              "Workload": "PowerBI",
              "UserId": "john@contoso.com",
              "ClientIP": "131.107.160.240",
              "CapacityId": "zy5bad4z-x1a2-491a-9f0c-f012171ee02e",
              "CapacityName": "Shared On Premium - Reserved",
              "WorkspaceId": "bf10ae91-c4f6-494e-b538-e2454229a765"
            }
          ],
          "continuationUri": "https://api.powerbi.com/v1.0/myorg/admin/activityevents?continuationToken='%2BRID%3A244SAKlHY7YQAAAAAAAAAA%3D%3D%23RT%3A1%23TRC%3A5%23FPC%3AARAAAAAAAAAAFwAAAAAAAAA%3D'",
          "continuationToken": "%2BRID%3A244SAKlHY7YQAAAAAAAAAA%3D%3D%23RT%3A1%23TRC%3A5%23FPC%3AARAAAAAAAAAAFwAAAAAAAAA%3D"
        }
        """,
        """
        {
          "activityEventEntities": [
            {
              "Id": "91ce06d1-d81b-4ea0-bc6d-2ce3dd2f8e87",
              "CreationTime": "2019-08-13T08:55:15",
              "Operation": "ViewReport",
              "OrganizationId": "d43e3248-3d83-44aa-a94d-c836bd7f9b79",
              "UserKey": "1236",
              "Activity": "ViewReport",
              "Workload": "PowerBI",
              "UserId": "john@contoso.com",
              "ClientIP": "127.0.0.1"
            },
            {
              "Id": "g632bb64-70fc-4e80-88f3-9fc2cdcacce8",
              "CreationTime": "2019-08-13T09:55:10",
              "Operation": "ViewReport",
              "OrganizationId": "e43e3248-3d83-44aa-a94d-c836bd7f9b79",
              "UserKey": "42343KJK55J",
              "Activity": "ViewReport",
              "Workload": "PowerBI",
              "UserId": "john@contoso.com",
              "ClientIP": "131.107.160.240",
              "CapacityId": "zy5bad4z-x1a2-491a-9f0c-f012171ee02e",
              "CapacityName": "Shared On Premium - Reserved",
              "WorkspaceId": "bf10ae91-c4f6-494e-b538-e2454229a765"
            }
          ],
          "continuationUri": "https://api.powerbi.com/v1.0/myorg/admin/activityevents?continuationToken='%2BRID%$4Z244SAKlHY7YQAAAAAAAAAA%3D%3D%23RT%3A1%23TRC%3A5%23FPC%3AARAAAAAAAAAAFwAAAAAAAAA%3D'",
          "continuationToken": "%2BRID%$4Z244SAKlHY7YQAAAAAAAAAA%3D%3D%23RT%3A1%23TRC%3A5%23FPC%3AARAAAAAAAAAAFwAAAAAAAAA%3D"
        }
        """,
        """
    {
      "activityEventEntities": [
        {
          "Id": "8fb974dc-739e-41e4-a219-b5801e28095e",
          "RecordType": 20,
          "CreationTime": "2023-05-23T08:06:47",
          "Operation": "GetSnapshots",
          "OrganizationId": "98c45f19-7cac-4002-8702-97d943a5ccb4",
          "UserType": 0,
          "UserKey": "10033FFF8929F27A",
          "Workload": "PowerBI",
          "UserId": "abc@contoso.onmicrosoft.com",
          "ClientIP": "185.175.34.186",
          "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50",
          "Activity": "GetSnapshots",
          "IsSuccess": true,
          "RequestId": "ee4b5af1-9aa3-34fe-a163-7b188e865ef1",
          "ActivityId": "cc1db5c9-ca04-484e-a6f2-f21de20bc000",
          "ModelsSnapshots": []
        },
        {
          "Id": "1db4c464-3e5d-4a89-b412-c2ce6fbae88e",
          "CreationTime": "2023-05-23T08:43:34",
          "Operation": "ViewReport",
          "ClientIP": "122.172.83.253",
          "Activity": "ViewReport",
          "ItemName": "Capacity Metrics Analysis",
          "WorkSpaceName": "Premium Capacity Utilization And Metrics 5/19/2023 11:57:07 AM",
          "DatasetName": "Capacity Metrics Analysis",
          "ReportName": "Capacity Metrics Analysis",
          "CapacityId": "zy5bad4z-x1a2-491a-9f0c-f012171ee02e",
          "CapacityName": "Shared On Premium - Reserved",
          "WorkspaceId": "bf10ae91-c4f6-494e-b538-e2454229a765",
          "AppName": "Premium Capacity Utilization And Metrics",
          "ObjectId": "fb8a915c-b720-4a77-9e55-3a12fc42efcd",
          "DatasetId": "5760cb34-a245-4eb7-a4e3-4ecae264a577",
          "ReportId": "ae596344-7fe6-43cb-baa7-c7ddc63271c8",
          "ArtifactId": "ae596344-7fe6-43cb-baa7-c7ddc63271c8",
          "ArtifactName": "Capacity Metrics Analysis",
          "ReportType": "PowerBIReport",
          "RequestId": "9b8a4e32-b0c8-febf-c3c3-f25d45f682a4",
          "ActivityId": "67c2dd35-242a-7053-4e92-8a7d78db9704",
          "AppReportId": "3f87e0bd-a95d-40a4-bab5-5e206d643f8f",
          "DistributionMethod": "Apps",
          "ConsumptionMethod": "Power BI Web",
          "ArtifactKind": "Report"
        }
      ],
      "continuationUri": null,
      "continuationToken": null
    }
    """,
    ]


@pytest.fixture
def add_dashboard():
    return """
    {
      "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "displayName": "SalesMarketing",
      "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "isReadOnly": false
    }
    """


@pytest.fixture
def add_dashboard_in_group():
    return """
    {
      "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "displayName": "SalesMarketing",
      "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48",
      "isReadOnly": false
    }
    """


@pytest.fixture
def get_dashboard():
    return """
    {
      "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "displayName": "SalesMarketing",
      "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "isReadOnly": false
    }
    """


@pytest.fixture
def get_dashboard_in_group():
    return """
    {
      "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
      "displayName": "SalesMarketing",
      "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48",
      "isReadOnly": false
    }
    """


@pytest.fixture
def get_modified_workspaces():
    return """
    [
      {
        "Id": "3740504d-1f93-42f9-8e9d-c8ba9b787a3b"
      },
      {
        "Id": "19cb346c-9839-4e19-81e6-76364d0b836f"
      }
    ]
    """


@pytest.fixture
def post_workspace_info():
    return """
    {
      "id": "e7d03602-4873-4760-b37e-1563ef5358e3",
      "createdDateTime": "2020-06-15T16:46:28.0487687Z",
      "status": "NotStarted"
    }
    """


@pytest.fixture
def get_scan_status():
    return """
    {
      "id": "e7d03602-4873-4760-b37e-1563ef5358e3",
      "createdDateTime": "2020-06-15T16:46:28.0487687Z",
      "status": "Succeeded"
    }
    """


@pytest.fixture
def get_scan_result():
    return """
    {
      "workspaces": [
        {
          "id": "d507422c-8d6d-4361-ac7a-30074a8cd0a1",
          "name": "V2 shared",
          "type": "Workspace",
          "state": "Active",
          "isOnDedicatedCapacity": true,
          "capacityId": "0f084df7-c13d-451b-af5f-ed0c466403b2",
          "defaultDatasetStorageFormat": "Small",
          "reports": [
            {
              "id": "c6d072d1-ed20-4b60-8329-16c4b934203b",
              "name": "CompositeModelParams-RLS",
              "datasetId": "132593c4-bf8d-4548-8f25-1ebb16a1613c",
              "createdDateTime": "2020-06-16T08:22:49.14",
              "modifiedDateTime": "2020-06-16T08:22:49.14",
              "modifiedBy": "john@contoso.com",
              "reportType": "PaginatedReport",
              "endorsementDetails": {
                "endorsement": "Certified",
                "certifiedBy": "john@contoso.com"
              },
              "sensitivityLabel": {
                "labelId": "85b38049-4259-43a2-8feb-244e222d96c0"
              },
              "users": [
                {
                  "displayName": "John Nick",
                  "emailAddress": "john@contoso.com",
                  "appUserAccessRight": "ReadExplore",
                  "identifier": "john@contoso.com",
                  "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
                  "principalType": "User"
                }
              ]
            }
          ],
          "dashboards": [
            {
              "id": "80814ece-9302-49e3-b6bc-bad2f7a86c1a",
              "displayName": "CompositeModelParamsDashboard",
              "isReadOnly": false,
              "tiles": [
                {
                  "id": "e687cc21-5b32-48f5-8c5e-4b844f190579",
                  "title": "CompositeModelParamsDashboard",
                  "reportId": "c6d072d1-ed20-4b60-8329-16c4b934203b",
                  "datasetId": "132593c4-bf8d-4548-8f25-1ebb16a1613c"
                }
              ],
              "sensitivityLabel": {
                "labelId": "d9b9581a-0594-4c39-81c5-91ddf40baeda"
              },
              "users": [
                {
                  "displayName": "John Nick",
                  "emailAddress": "john@contoso.com",
                  "appUserAccessRight": "ReadExplore",
                  "identifier": "john@contoso.com",
                  "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
                  "principalType": "User"
                }
              ]
            }
          ],
          "datasets": [
            {
              "id": "e7e8a355-e77b-4418-a7b8-ae5972fdaa03",
              "name": "ExportB",
              "tables": [
                {
                  "name": "DW_Revenues",
                  "columns": [
                    {
                      "name": "RowNumber-2662979B-1795-4F74-8F37-6A1BA8059B61",
                      "dataType": "Int64",
                      "isHidden": true
                    }
                  ],
                  "measures": [
                    {
                      "name": "MyMeasure",
                      "expression": "CALCULATE(SELECTEDVALUE('DW_Revenues DW_RevenuesTestToBeDeleted'[Numbers])*10)",
                      "description": "My measure",
                      "isHidden": false
                    }
                  ],
                  "isHidden": false,
                  "description": "My table",
                  "source": [
                    {
                      "expression": "let\\n    Source = Revenues,\\n    Param = RevenuesParam\\nin\\n    Source"
                    }
                  ]
                }
              ],
              "relationships": [],
              "configuredBy": "john@contoso.com",
              "targetStorageMode": "Abf",
              "endorsementDetails": {
                "endorsement": "Certified",
                "certifiedBy": "john@contoso.com"
              },
              "expressions": [
                {
                  "name": "Revenues",
                  "description": "revenues",
                  "expression": "let\\n    Source = Sql.Database(\\"sqlserver.database.windows.net\\", \\"DB\\"),\\n    RevenuesTable = Source{[Schema=\\"DB_SCHEMA\\",Item=\\"DB_SCHEMA_ITEM\\"]}[Data]\\nin\\n    RevenuesTable"
                },
                {
                  "name": "RevenuesParam",
                  "description": "revenues param",
                  "expression": "\\"revenues param value\\" meta [IsParameterQuery=true, Type=\\"Text\\", IsParameterQueryRequired=true]"
                }
              ],
              "roles": [
                {
                  "name": "Teams",
                  "modelPermission": "Read",
                  "members": [
                    {
                      "memberName": "john@contoso.com",
                      "memberId": "ee96296b-fb71-4f65-a8af-c0ec5a7daced",
                      "memberType": "User",
                      "identityProvider": "AzureAD"
                    },
                    {
                      "memberName": "group@contoso.com",
                      "memberId": "0a1cdbc3-f82c-4001-8b96-be04ae9d25a3",
                      "memberType": "Group",
                      "identityProvider": "AzureAD"
                    }
                  ],
                  "tablePermissions": [
                    {
                      "name": "DW_Revenues DW_RevenuesTest",
                      "filterExpression": "[InTeams] = \\"True\\""
                    }
                  ]
                }
              ],
              "upstreamDataflows": [
                {
                  "targetDataflowId": "a842dbb1-32ca-46b0-9648-498b2c2d5e38",
                  "groupId": "b7416115-7421-42c0-b525-1505ce40d2f0"
                },
                {
                  "targetDataflowId": "06898194-2eaf-4122-bacc-133db1f8585d",
                  "groupId": "7263838d-80d7-4b8d-a1f6-50fc27e74a97"
                }
              ],
              "datasourceUsages": [
                {
                  "datasourceInstanceId": "c79ad907-df19-43fe-a0f7-d9f365d67070"
                }
              ],
              "misconfiguredDatasourceUsages": [
                {
                  "datasourceInstanceId": "80ec28bc-fe81-43ea-be52-a07a95cfbcab"
                }
              ],
              "sensitivityLabel": {
                "labelId": "bf3dc57d-d796-41c0-bbe9-a47f5ee3331e"
              },
              "users": [
                {
                  "displayName": "John Nick",
                  "emailAddress": "john@contoso.com",
                  "appUserAccessRight": "ReadExplore",
                  "identifier": "john@contoso.com",
                  "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
                  "principalType": "User"
                }
              ]
            }
          ],
          "dataflows": [
            {
              "objectId": "a842dbb1-32ca-46b0-9648-498b2c2d5e38",
              "name": "Azure SQL",
              "description": "Azure SQL dataflow",
              "configuredBy": "john@contoso.com",
              "modifiedBy": "john@contoso.com",
              "modifiedDateTime": "2020-06-16T08:27:47.783Z",
              "endorsementDetails": {
                "endorsement": "Certified",
                "certifiedBy": "john@contoso.com"
              },
              "datasourceUsages": [
                {
                  "datasourceInstanceId": "c79ad907-df19-43fe-a0f7-d9f365d67070"
                }
              ],
              "misconfiguredDatasourceUsages": [
                {
                  "datasourceInstanceId": "80ec28bc-fe81-43ea-be52-a07a95cfbcab"
                }
              ],
              "sensitivityLabel": {
                "labelId": "5c9f8c24-2a94-4fd2-a105-9a8b096c5af1"
              },
              "users": [
                {
                  "displayName": "John Nick",
                  "emailAddress": "john@contoso.com",
                  "appUserAccessRight": "ReadExplore",
                  "identifier": "john@contoso.com",
                  "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
                  "principalType": "User"
                }
              ]
            }
          ],
          "datamarts": [
            {
              "id": "9df8d63c-db5b-44c3-a8e3-9f8c8ec1eec2",
              "name": "MyDatamart",
              "description": "SQL datamart",
              "type": "Sql",
              "configuredBy": "john@contoso.com",
              "configuredById": "5c9f8c24-2a94-4fd2-a105-9a8b096cdsew",
              "modifiedBy": "john@contoso.com",
              "modifiedDateTime": "2020-06-16T08:27:47.783Z",
              "sensitivityLabel": {
                "labelId": "5c9f8c24-2a94-4fd2-a105-9a8b096c5af1"
              },
              "endorsementDetails": {
                "endorsement": "Certified",
                "certifiedBy": "john@contoso.com"
              },
              "UpstreamDataflows": [
                {
                  "targetDataflowId": "5c9f8c24-2a94-34fd-a105-9a8b096c4555",
                  "groupId": "5c9f8c24-4dsc-4fd2-a105-9a8b096c4fgt"
                }
              ],
              "datasourceUsages": [
                {
                  "datasourceInstanceId": "c79ad907-df19-43fe-a0f7-d9f365d67070"
                }
              ],
              "Users": [
                {
                  "displayName": "John Nick",
                  "emailAddress": "john@contoso.com",
                  "identifier": "john@contoso.com",
                  "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
                  "principalType": "User",
                  "userType": "User",
                  "profile": {
                    "id": "45416453",
                    "displayName": "John's profile"
                  },
                  "datamartUserAccessRight": "Read"
                }
              ]
            }
          ],
          "users": [
            {
              "displayName": "John Nick",
              "emailAddress": "john@contoso.com",
              "appUserAccessRight": "ReadExplore",
              "identifier": "john@contoso.com",
              "graphId": "3fadb6e4-130c-4a8f-aeac-416e38b66756",
              "principalType": "User"
            }
          ]
        }
      ],
      "datasourceInstances": [
        {
          "datasourceType": "Sql",
          "connectionDetails": {
            "server": "qlserver.database.windows.net",
            "database": "dbo.largest_table"
          },
          "datasourceId": "c79ad907-df19-43fe-a0f7-d9f365d67070",
          "gatewayId": "e820592e-f8cf-4a6f-b1ed-566799d29565"
        }
      ],
      "misconfiguredDatasourceInstances": [
        {
          "datasourceType": "Sql",
          "connectionDetails": {
            "server": "sqlserver.database.windows.net",
            "database": "dbo.table"
          },
          "datasourceId": "80ec28bc-fe81-43ea-be52-a07a95cfbcab",
          "gatewayId": "505a19c1-4190-4e8e-a4f6-dd72722feced"
        }
      ]
    }
    """
