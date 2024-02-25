# How to contribute

Contributions such as bug reports, fixes, documentation, enhancements, and ideas are welcome.

## Reporting Bugs

Use the [Issues tab](https://github.com/andrewvillazon/pbipy/issues) to report any bugs. Be sure to include:

* A quick summary or background.

* Steps to reproduce.

* What you expected would happen.

* What actually happens?

* Sample code if you can, with error messages or the stack trace.

* Notes (possibly including why you think this might be happening or stuff you tried that didn't work).

* Lastly, avoid including sensitive information with bug reports, such as authentication tokens or data that might be commercially sensitive.

If you know how to fix the bug or have written a fix, even better! See below for how to submit changes.

## Adding a new feature, modifying an existing one, or patching bugs

If you'd like to work on something, there's no need to ask for permission, but here are a couple of things to consider:

* Have a quick check in the [Issues](https://github.com/andrewvillazon/pbipy/issues) to see if it's not already being discussed or worked on.

* Create an Issue to associate with the change to track some of the thinking and rationale behind the change.

### Library Design

Start reading the code, and you'll get the hang of it. Here are some resources to help understand the influences on the library design:

* [What makes a good API wrapper?](https://wynnnetherland.com/journal/what-makes-a-good-api-wrapper) - `pbipy` aims to be more idiomatic and consistent with Python and its conventions.

* See the Python jira library's [`JIRA` class](https://github.com/pycontribs/jira/blob/ff6985b7a9efff6b7b72490a4f8c61c398152796/jira/client.py#L327) as an example of how `pbipy` tries to name methods that wrap API endpoints.

### Testing

All code contributions should have associated tests. Because the library is an API wrapper, most of the tests check that:

* URLs are formed properly

* Request data is handled and passed to the API correctly.

* API responses are parsed as expected.

`pbipy` uses the [responses](https://github.com/getsentry/responses) library to validate HTTP requests and to mock HTTP responses.

#### Test Data

Tests generally use the sample responses found in the documentation for each API endpoint. 

Sometimes, the API documentation does not provide a sample response, or you may want to create your own test data. When creating test data, try to mimic the data as it would be in a Power BI instance and, for security reasons, avoid including actual values from your own Power BI instances.

### Docstrings

Any new functions, methods, classes, and modules should include docstrings. Docstrings follow the numpy style guide. Currently, pbipy does not have dedicated documentation, so docstrings are the next best option.

### Formatting

`pbipy` uses [black](https://github.com/psf/black) for formatting.

## Thank You

`pbipy` is a volunteer effort. Thanks for taking the time to contribute.
