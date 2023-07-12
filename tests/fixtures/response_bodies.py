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
      "value": [
        {
          "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
          "isReadOnly": false,
          "isOnDedicatedCapacity": false,
          "name": "sample group"
        }
      ]
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
