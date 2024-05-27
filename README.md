# pbipy

![PyPI](https://img.shields.io/pypi/v/pbipy) ![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/andrewvillazon/pbipy) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pbipy) ![GitHub](https://img.shields.io/github/license/andrewvillazon/pbipy) ![Static Badge](https://img.shields.io/badge/Python-blue?logo=python&logoColor=yellow) ![Static Badge](https://img.shields.io/badge/power-bi-yellow?logoColor=yellow&labelColor=yellow&color=black)


`pbipy` is a Python Library for interacting with the Power BI Rest API. It aims to simplyify working with the Power BI Rest API and support programatic administration of Power BI in Python.

`pbipy` supports operations for Apps, Dataflows, Datasets, Reports, and Workspaces (Groups), allowing users to perform actions on their PowerBI instance using Python.

## Installation

```console
pip install pbipy
```

Or to install the latest development code:

```console
pip install git+https://github.com/andrewvillazon/pbipy
```

## Getting Started: Authentication

To use `pbipy` you'll first need to acquire a `bearer_token`.

*How do I get a `bearer_token`?*

To acquire a `bearer_token` you'll need to authenticate against your [Registered Azure Power BI App](https://learn.microsoft.com/en-us/power-bi/developer/embedded/register-app?tabs=customers). Registering is the first step in turning on the Power BI Rest API, so from here on it's assumed your Power BI Rest API is up and running.

To authenticate against the Registered App, Microsoft provides the `MSAL` and `azure-identity` python libraries. These libraries support different ways of acquiring a `bearer_token` and which to use will depend on how your cloud/tenant is configured.

Because there are multiple ways to acquire the token, `pbipy` leaves it up to the user do this in the way that suits, rather than directly handling authentication (of course, this might change in future).

This `README` doesn't cover authentication in detail, however, these are some helpful resources that look at acquiring a `bearer_token` in the context of Power BI:

* [Power BI REST API with Python and MSAL. Part II.](https://www.datalineo.com/post/power-bi-rest-api-with-python-and-msal-part-ii)
* [Power BI REST API with Python Part III, azure-identity](https://www.datalineo.com/post/power-bi-rest-api-with-python-part-iii-azure-identity)
* [Monitoring Power BI using REST APIs from Python](https://data-goblins.com/power-bi/power-bi-api-python)

The example below uses the `msal` library to to get a bearer_token.

```python
import msal


#  msal auth setup
def acquire_bearer_token(username, password, azure_tenant_id, client_id, scopes):
    app = msal.PublicClientApplication(client_id, authority=azure_tenant_id)
    result = app.acquire_token_by_username_password(username, password, scopes)
    return result["access_token"]


bearer_token = acquire_bearer_token(
    username="your-username",
    password="your-password",
    azure_tenant_id="https://login.microsoftonline.com/your-azure-tenant-id",
    client_id="your-pbi-client-id",
    scopes=["https://analysis.windows.net/powerbi/api/.default"],
)
```

The code that follows assumes you've authenticated and acquired your `bearer_token`.

## Useage

Start by creating the `PowerBI()` client. Interactions with the Power BI Rest API go through this object. 

```python
from pbipy import PowerBI

pbi = PowerBI(bearer_token)
```

To interact with the API, simply call the relevant method from the client.

```python
# Grab the datasets from a workspace

pbi.datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")
```

`pbipy` converts API responses into regular Python objects, with snake case included! 🐍🐍

```python
sales = pbi.dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

print(type(sales))
print(hasattr(sales, "configured_by"))

# <class 'pbipy.Dataset'>
# True
```

Most methods take in an object id...

```python
dataset = pbi.dataset(
    id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    group="a2f89923-421a-464e-bf4c-25eab39bb09f"
)
```

... or just pass in the object itself.

```python
group = pbi.group("a2f89923-421a-464e-bf4c-25eab39bb09f")

dataset = pbi.dataset(
    "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    ,group=group
)
```

If you need to access the raw json representation, this is supported to.

```python
sales = pbi.dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

print(sales.raw)

# {
#   "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
#   "name": "SalesMarketing",
#   "addRowsAPIEnabled": False,
#   "configuredBy": "john@contoso.com",
#   ...
# }
```

## Example: Working with Datasets

Let's see how `pbipy` works by performing some operations on a Dataset.

First, we initialize our client.

```python
from pbipy import PowerBI

pbi = PowerBI(bearer_token)
```

Now that we've got a client, we can load a Dataset from the API. To load a Dataset, we call the `dataset()` method with an `id` and `group` argument. In the Power BI Rest API, a **Group** and **Workspace** are synonymous and used interchangeably.

```python
sales = pbi.dataset(
    id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
)

print(sales)

# <Dataset id='cfafbeb1-8037-4d0c-896e-a46fb27ff229', name='SalesMarketing', ...>
```

Dataset not updating? Let's look at the Refresh History. 

We call the `refresh_history()` method on our Dataset. Easy.

```python
refresh_history = sales.refresh_history()

for entry in refresh_history:
    print(entry)

# {"refreshType":"ViaApi", "startTime":"2017-06-13T09:25:43.153Z", "status": "Completed" ...}
```

Need to kick off a refresh? That's easy too.

```python
sales.refresh()
```

How about adding some user permissions to our Dataset? Just call the `add_user()` method with the User's details and permissions.

```python
# Give John 'Read' access on the dataset
sales.add_user("john@contoso.com", "User", "Read")
```

Lastly, if we're feeling adventurous, we can execute DAX against a Dataset and use the results in Python.

```python
dxq_result = sales.execute_queries("EVALUATE VALUES(MyTable)")
print(dxq_result)

# {
#   "results": [
#     {
#       "tables": [
#         {
#           "rows": [
#             {
#               "MyTable[Year]": 2010,
#               "MyTable[Quarter]": "Q1"
#             },
# ...
# }
```

## Example: Working with the Admin object

`pbypi` also supports [Administrator Operations](https://learn.microsoft.com/en-us/rest/api/power-bi/admin), specialized operations available to users with Power BI Admin rights. Let's see how we can use these.

First, we need to initialize our client. Then we call the `admin` method and initialize an `Admin` object.

```python
from pbipy import PowerBI

pbi = PowerBI(bearer_token)
admin = pbi.admin()
```

Need to review some access on some reports? We can call the `report_users` method.

```python
users = admin.report_users("5b218778-e7a5-4d73-8187-f10824047715")
print(users[0])

# {"displayName": "John Nick", "emailAddress": "john@contoso.com", ...}
```

What about understanding User activity on your Power BI tenant?

```python
from datetime import datetime

start_dtm = datetime(2019, 8, 31, 0, 0, 0)
end_dtm = datetime(2019, 8, 31, 23, 59, 59)

activity_events = admin.activity_events(start_dtm, end_dtm)

print(activity_events)

# [
#   {
#       "Id": "41ce06d1", 
#       "CreationTime": "2019-08-13T07:55:15", 
#       "Operation": "ViewReport", 
#       ...
#   },
#   {
#       "Id": "c632aa64", 
#       "CreationTime": "2019-08-13T07:55:10", 
#       "Operation": "GetSnapshots", 
#       ...
#   }
# ]
```

## More examples

### Datasets in a Workspace

```python
datasets = pbi.datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

for dataset in datasets:
    print(dataset)

# <Dataset id='cfafbeb1-8037-4d0c-896e-a46fb27ff229', ...>
# <Dataset id='f7fc6510-e151-42a3-850b-d0805a391db0', ...>
```

### List Workspaces

```python
groups = pbi.groups()

for group in groups:
    print(group)

# <Group id='a2f89923-421a-464e-bf4c-25eab39bb09f', name='contoso'>
# <Group id='3d9b93c6-7b6d-4801-a491-1738910904fd', name='marketing'>
```

### Create a Workspace

```python
group = pbi.create_group("contoso")
print(group)

# <Group id='a2f89923-421a-464e-bf4c-25eab39bb09f', name='contoso'>
```

### Users and their access

```python
group = pbi.group("a2f89923-421a-464e-bf4c-25eab39bb09f")
users = group.users()

for user in users:
    print(user)

# {"identifier": "john@contoso.com", "groupUserAccessRight": "Admin", ... }
# {"identifier": "Adam@contoso.com", "groupUserAccessRight": "Member", ... }
```

## Power BI Rest API Operations

`pbipy` methods wrap around the Operations described in the Power BI Rest API Reference:

[Power BI REST APIs for embedded analytics and automation - Power BI REST API](https://learn.microsoft.com/en-us/rest/api/power-bi/)


## What's implemented?

Most of the core operations on Datasets, Workspaces (Groups), Reports, Apps, and Dataflows are implemented. Given the many available endpoints, not everything is covered by `pbipy`, so expect a few features to be missing.

If an operation is missing and you think it'd be useful, feel free to suggest it on the [Issues tab](https://github.com/andrewvillazon/pbipy/issues).

| PowerBI Component   	| Progress 	| Notes 	                                                                            |
|---------------------	|----------	|-------------------------------------------------------------------------------------- |
| Datasets            	| Done     	|       	                                                                            |
| Groups (Workspaces) 	| Done    	|       	                                                                            |
| Reports             	| Done      |       	                                                                            |
| Apps                	| Done   	|       	                                                                            |
| Dataflows           	| Done    	|       	                                                                            |
| Admin Operations     	| Done    	| Implements operations related to Datasets, Groups, Reports, Apps, and Dataflows only. |
| Dashboards          	| Todo     	|       	                                                                            |
| Everything else     	| Backlog  	|       	                                                                            |

## Contributing

`pbipy` is an open source project. Contributions such as bug reports, fixes, documentation or docstrings, enhancements, and ideas are welcome. `pbipy` uses github to host code, track issues, record feature requests, and accept pull requests.

View [CONTRIBUTING.md](https://github.com/andrewvillazon/pbipy/blob/master/CONTRIBUTING.md) to learn more about contributing.

## Acknowledgements

The design of this library was heavily inspired by (basically copied) the [pycontribs/jira](https://github.com/pycontribs/jira) library. It also borrows elements of [cmberryay's pypowerbi wrapper](https://github.com/cmberryau/pypowerbi).

Thank You to all the contributors to these libraries for the great examples of what an API Wrapper can be.