# pbipy

![GitHub](https://img.shields.io/github/license/andrewvillazon/pbipy)

A Power BI Rest API wrapper for Python. 

`pbipy` aims to simplyify working with the Power BI Rest API and support programatic administration of Power BI in Python.

**NOTE:** `pbipy` is currently in active development so not all API functionality is supported yet. See below for what's been implemented and what's coming.

## Installation

```console
pip install pbipy
```


## Getting Started: Authentication

To use `pbipy` you'll first need to acquire a `bearer_token`.

*How do I get a `bearer_token`?*

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

### Functionality

To interact with the API, simply call the relevant method from the client.

```python
```

Most methods support passing in an object id...

```python
```

... or just pass in the object itself.

```python
```

`pbipy` converts Rest API responses into regular Python objects (snake case included).

```python
```

To make life easier, attributes are also translated into sensible types.

```python
```

And if you need to access the raw json representation, this is supported to.

```python
```

## Examples

### Fetch a Dataset

```python
```

### Refresh History

```python
```

### Add user permissions for a Dataset

```python
```

## Power BI Rest API Operations

`pbipy` methods are roughly organized around the Operations of the Power BI Rest API:

[Power BI REST APIs for embedded analytics and automation - Power BI REST API](https://learn.microsoft.com/en-us/rest/api/power-bi/)


## What's implemented?

`pbipy` is in the early stages of development and not all API functionality is currently available. Check back regularly to see what's been added or still in the pipeline.

| Operation Group 	| Development State     	| Notes 	|
|-----------------	|-----------------------	|-------	|
| Datasets        	| Partially Implemented 	|       	|

## Acknowledgements

The design of this library was heavily inspired by (basically copied) the [pycontribs/jira](https://github.com/pycontribs/jira) library. It also borrows elements of [cmberryay's pypowerbi wrapper](https://github.com/cmberryau/pypowerbi).

Thank You to all the contributors to these libraries for the great examples of what an API Wrapper can be.