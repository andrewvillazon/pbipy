# pbipy

A Power BI Rest API wrapper for Python. 

`pbipy` aims to simplyify working with the Power BI Rest API and support programatic administration of Power BI in Python.

**NOTE:** At the moment `pbipy` is only implementing `GET` based methods, i.e., getting data from the Rest API. Functionality to update and create new items on the Power BI Instance will be implemented soon.

## Installation

```console
pip install pbipy
```


## Authentication

To use `pbipy` you'll first need to acquire a `bearer_token`.

How do I get a `bearer_token`?

To acquire a `bearer_token` you'll need to authenticate against your [Registered Azure Power BI App](https://learn.microsoft.com/en-us/power-bi/developer/embedded/register-app?tabs=customers). Registering is the first step in turning on the Power BI Rest API, so from this point on we're assuming that registration is taken care of.

To authenticate against the Registered App, Microsoft provides the `MSAL` and `azure-identity` python libraries. These libraries support many different ways of acquiring a `bearer_token`.

Because there are multiple ways to acquire the token, `pbipy` assumes you'll do this in the way that suits, rather than directly handling authentication (of course, this might change in future).

This `README` doesn't cover Authentication in detail, however, these are some helpful resources that look at acquiring a `bearer_token` in the context of Power BI:

* [Power BI REST API with Python and MSAL. Part II.](https://www.datalineo.com/post/power-bi-rest-api-with-python-and-msal-part-ii)
* [Power BI REST API with Python Part III, azure-identity](https://www.datalineo.com/post/power-bi-rest-api-with-python-part-iii-azure-identity)
* [Monitoring Power BI using REST APIs from Python](https://data-goblins.com/power-bi/power-bi-api-python)

See below for an example that uses the `msal` library.

## Using pbipy

Start by creating the `PowerBI()` client. All interactions with the Power BI Rest API go through this object. 

The example uses `msal` authentication methods to get a `bearer_token`.
```python
import msal

from pbipy import PowerBI


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

### Operation Groups

`pbipy` methods are organized into Operation Groups that mirror the operation groups of the Power BI Rest API:

[REST Operation Groups](https://learn.microsoft.com/en-us/rest/api/power-bi/#rest-operation-groups)

For example:

```python
pbi.groups.get_groups()
pbi.datasets.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")
...
```

### Functionality

To interact with the API, simply call the relevant method from the client.

```python
groups = pbi.groups.groups.get_groups()
print(groups[0])

# Group(id='3d9b93c6-7b6d-4801-a491-1738910904fd', name='marketing group', type='Workspace', ...)
```

Most methods support passing in an object id...

```python
refresh_history = pbi.datasets.get_refresh_history("cfafbeb1-8037-4d0c-896e-a46fb27ff229")
print(refresh_history[0])

# Refresh(id=None, request_id='9399bb89-25d1-44f8-8576-136d7e9014b1', refresh_type='ViaApi', ...)
```

... or just pass in the object itself.

```python
sales = pbi.datasets.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")
refresh_history = pbi.datasets.get_refresh_history(sales)
print(refresh_history[0])

# Refresh(id=None, request_id='9399bb89-25d1-44f8-8576-136d7e9014b1', refresh_type='ViaApi', ...)
```

`pbipy` converts API responses into Python objects.

```python
sales = pbi.datasets.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")
print(type(sales))

# <class 'pbipy.models.Dataset'>
```

To make life easier, attributes are also translated into sensible types.

```python
sales = pbi.datasets.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")
print(isinstance(sales.created_date, datetime))

# True
```

Objects are standardized to have consistent attributes, even when a key is missing from an API response.

```python
sales = Dataset(id="cfafbeb1-8037-4d0c-896e-a46fb27ff229", name="SalesMarketing")

print(hasattr(sales, "is_refreshable"))
print(sales.is_refreshable)

# True
# None
```

And if you need to access the raw json representation, this is supported to.

```python
sales = pbi.datasets.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")
print(sales.raw)

# {'id': 'cfafbeb1-8037-4d0c-896e-a46fb27ff229', 'name': 'SalesMarketing', 'addRowsAPIEnabled': False, ...},
```

## Power BI Rest API Reference

In general, most of the `PowerBI()` methods follow the resources laid out in the Power BI Rest API Reference:

[Power BI REST APIs for embedded analytics and automation - Power BI REST API](https://learn.microsoft.com/en-us/rest/api/power-bi/)

## Acknowledgements

The design of this library was inspired by the [pycontribs/jira](https://github.com/pycontribs/jira) library. It also borrows elements of [cmberryay's pypowerbi wrapper](https://github.com/cmberryau/pypowerbi). A personal Thank You to all the contributors to these libraries for the great examples of what an API Wrapper can be.