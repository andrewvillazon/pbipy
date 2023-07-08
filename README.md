# pbipy

![PyPI](https://img.shields.io/pypi/v/pbipy) ![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/andrewvillazon/pbipy) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pbipy) ![GitHub](https://img.shields.io/github/license/andrewvillazon/pbipy) ![Static Badge](https://img.shields.io/badge/Python-blue?logo=python&logoColor=yellow) ![Static Badge](https://img.shields.io/badge/power-bi-yellow?logoColor=yellow&labelColor=yellow&color=black)


`pbipy` is a Python Library for interacting with the Power BI Rest API. It aims to simplyify working with the Power BI Rest API and support programatic administration of Power BI in Python.

`pbipy` supports operations for Apps, Dataflows, Datasets, Reports, and Workspaces (Groups), allowing users to perform actions on their PowerBI instance using Python.

See [development progress](#development-progress) below for what's been implemented and what's coming.

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

To acquire a `bearer_token` you'll need to authenticate against your [Registered Azure Power BI App](https://learn.microsoft.com/en-us/power-bi/developer/embedded/register-app?tabs=customers). Registering is the first step in turning on the Power BI Rest API, so from this point on it's assumed your Power BI Rest API is up and running.

To authenticate against the Registered App, Microsoft provides the `MSAL` and `azure-identity` python libraries. These libraries support many different ways of acquiring a `bearer_token`.

Because there are multiple ways to acquire the token, `pbipy` assumes you'll do this in the way that suits, rather than directly handling authentication (of course, this might change in future).

This `README` doesn't cover Authentication in detail, however, these are some helpful resources that look at acquiring a `bearer_token` in the context of Power BI:

* [Power BI REST API with Python and MSAL. Part II.](https://www.datalineo.com/post/power-bi-rest-api-with-python-and-msal-part-ii)
* [Power BI REST API with Python Part III, azure-identity](https://www.datalineo.com/post/power-bi-rest-api-with-python-part-iii-azure-identity)
* [Monitoring Power BI using REST APIs from Python](https://data-goblins.com/power-bi/power-bi-api-python)

The example below uses the `msal` library to to get a `bearer_token`.

## Useage

Start by creating the `PowerBI()` client. All interactions with the Power BI Rest API go through this object. 

```python
import msal

from pbipy import PowerBI


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

# Create Client
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

# <class 'pbipy.resources.Dataset'>
# True
```

Most methods take in an object id...

```python
dataset = pbi.dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229", group="a2f89923-421a-464e-bf4c-25eab39bb09f")
```

... or just pass in the object itself.

```python
group = pbi.group("a2f89923-421a-464e-bf4c-25eab39bb09f")

dataset = pbi.dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229", group=group)
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

First, we need to load the Dataset from the API. To do this, we call the `dataset()` method from the `pbi` client we created above. 

The Power BI Rest API will look for the Dataset in the current user's workspace if we don't provide a `group` argument.

```python
sales = pbi.dataset(id="cfafbeb1-8037-4d0c-896e-a46fb27ff229")
print(sales)

# <Dataset id='cfafbeb1-8037-4d0c-896e-a46fb27ff229', name='SalesMarketing', ...>
```

But we likely want to target a Dataset in a *Workspace*. To do this, we provide the Workspace Id as the `group` argument when we call the `dataset()` method.

```python
sales = pbi.dataset(
    "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
)
```

Now that we've got our target Dataset let's look at its Refresh History. We call the `refresh_history()` method on our Dataset. Easy.

```python
dataset = pbi.dataset(
    "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
)

refresh_history = dataset.refresh_history()

for entry in refresh_history:
    print(entry)

# {"refreshType":"ViaApi", "startTime":"2017-06-13T09:25:43.153Z", "status": "Completed" ...}
```

How about adding some user permissions to our Dataset? That's easy too. Just call the `add_user()` method with the User's details and permissions.

```python
sales_ds = pbi.dataset( "cfafbeb1-8037-4d0c-896e-a46fb27ff229")

# Give John 'Read' access on the dataset
sales_ds.add_user("john@contoso.com", "User", "Read")
```

Lastly, if we're feeling adventurous, we can execute DAX against a Dataset and use the results in Python.

```python
dataset = pbi.dataset( "cfafbeb1-8037-4d0c-896e-a46fb27ff229")

dxq_result = dataset.execute_queries("EVALUATE VALUES(MyTable)")
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


## Development Progress

`pbipy` is in development so expect a few features to be missing. The aim is to cover off most of the core stuff like Datasets, Workspaces (Groups), Reports, Apps, etc., and the rest later on. Check back regularly to see what's been added or still in the pipeline.

| PowerBI Component   	| Progress 	| Notes 	|
|---------------------	|----------	|-------	|
| Datasets            	| Done     	|       	|
| Groups (Workspaces) 	| Done    	|       	|
| Reports             	| Done      |       	|
| Apps                	| Done   	|       	|
| Dataflows           	| Done    	|       	|
| Admin Operations     	| Doing    	|       	|
| Dashboards          	| Todo     	|       	|
| Everything else     	| Backlog  	|       	|

## Contributing

Contributions such as bug reports, fixes, documentation or docstrings, enhancements, and ideas are welcome. `pbipy` uses github to host code, track issues, record feature requests, and accept pull requests.

A `contributing.md` is in the works, but in the meantime below is a general guide.

### Making a contribution

Pull requests are the best way to make a contribution to the code:

1. Fork the repo and create your branch from master.
2. If you've added code that should be tested, add tests.
3. Add docstrings.
4. Ensure the test suite passes.
5. Format your code (`pbipy` uses [black](https://github.com/psf/black)).
6. Issue that pull request!

### Reporting a bug

Great Bug Reports tend to have:

* A quick summary and/or background
* Steps to reproduce. Be specific! Give sample code if you can.
* What you expected would happen
* What actually happens
* Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Acknowledgements

The design of this library was heavily inspired by (basically copied) the [pycontribs/jira](https://github.com/pycontribs/jira) library. It also borrows elements of [cmberryay's pypowerbi wrapper](https://github.com/cmberryau/pypowerbi).

Thank You to all the contributors to these libraries for the great examples of what an API Wrapper can be.