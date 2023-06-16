from pbipy import settings
from pbipy.utils import RequestsMixin, remove_no_values, to_snake_case


class Resource(RequestsMixin):
    BASE_URL = settings.BASE_URL

    def __init__(self, session, **kwargs) -> None:
        self.session = session
        self.raw = None

        if "group_id" in kwargs:
            group_id = kwargs.get("group_id")
            setattr(self, "group_id", group_id)

        if self.group_id:
            self.group_path = f"/groups/{self.group_id}"
        else:
            self.group_path = ""

        self._base_path = f"{self.BASE_URL}{self.group_path}"

    def _load_from_raw(self, raw):
        self.raw = raw

        for k, v in raw.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)

        return self

    def load(self):
        raw = self.get_raw(self.base_path, self.session)
        self._load_from_raw(raw)


class Dataset(Resource):
    def __init__(
        self,
        id,
        session,
        group_id=None,
        raw=None,
    ) -> None:
        self.id = id

        super().__init__(session, group_id=group_id)

        self.base_path = f"{self._base_path}/datasets/{self.id}"

        # Supports creating from a list of js, e.g., get_datasets endpoint
        if raw:
            self._load_from_raw(raw)

    def add_user(
        self,
        identifier: str,
        principal_type: str,
        access_right: str,
    ) -> None:
        """
        Grants the specified user's permissions to the specified dataset.

        Parameters
        ----------
        `identifier` : `str`
            For principal type `User`, provide the UPN. Otherwise provide
            the object ID of the principal.
        `principal_type` : `str`
            The principal type, e.g., "App", "Group", "None", or "User".
        `access_right` : `str`
            The Dataset User Access Right to grant to the user for the
            dataset, e.g.,"Read", "ReadExplore", "ReadReshare", or
            "ReadReshareExplore".
        """

        resource = self.base_path + "/users"
        dataset_user_access = {
            "identifier": identifier,
            "principalType": principal_type,
            "datasetUserAccessRight": access_right,
        }

        self.post(resource, self.session, dataset_user_access)

    def bind_to_gateway(
        self,
        gateway_object_id: str,
        datasource_object_ids: list = None,
    ) -> None:
        """
        Binds the specified dataset from MyWorkspace or group to the specified
        gateway, optionally with a given set of data source IDs. If you
        don't supply a specific data source ID, the dataset will be bound
        to the first matching data source in the gateway.

        Parameters
        ----------
        `gateway_object_id` : `str`
            The gateway ID. When using a gateway cluster, the gateway ID
            refers to the primary (first) gateway in the cluster and is
            similar to the gateway cluster ID.
        `datasource_object_ids` : `list`, optional
            The unique identifiers for the data sources in the gateway.
        """

        bind_to_gateway_request = {
            "gatewayObjectId": gateway_object_id,
            "datasourceObjectIds": datasource_object_ids,
        }

        if bind_to_gateway_request["datasourceObjectIds"] is None:
            bind_to_gateway_request.pop("datasourceObjectIds")

        resource = self.base_path + "/Default.BindToGateway"

        self.post(resource, self.session, bind_to_gateway_request)

    def cancel_refresh(
        self,
        refresh_id: str,
    ) -> None:
        """
        Cancels the specified refresh operation for the specified dataset
        from MyWorkspace or group.

        Parameters
        ----------
        `refresh_id` : `str`
            Refresh Id to cancel.
        """

        resource = self.base_path + f"/refreshes/{refresh_id}"
        self.delete(resource, self.session)

    def datasources(
        self,
    ) -> list[dict]:
        """
        Returns a list of datasources for the dataset.

        Returns
        -------
        `list[dict]`
            List of PowerBI datasources for the dataset.
        """

        resource = self.base_path + "/datasources"
        return self.get_raw(resource, self.session)

    def discover_gateways(
        self,
    ) -> list:
        """
        Returns a list of gateways that the specified dataset from My workspace
        can be bound to.

        This API call is only relevant to datasets that have at least one
        on-premises connection. For datasets with cloud-only connections,
        this API call returns an empty list.

        Returns
        -------
        `list`
            List of PowerBI Gateways that can be bound to.
        """

        resource = self.base_path + "/Default.DiscoverGateways"
        return self.get_raw(resource, self.session)

    def execute_queries(
        self,
        queries: str | list[str],
        impersonated_user_name: str = None,
        include_nulls: bool = None,
    ) -> dict:
        """
        Executes Data Analysis Expressions (DAX) queries against the provided
        dataset.

        DAX query errors will result in:

            A response error, such as DAX query failure.
            A failure HTTP status code (400).

        A query that requests more than one table, or more than the allowed
        number of table rows, will result in:

            Limited data being returned.
            A response error, such as More than one result table in a query
            or More than {allowed number} rows in a query result.

            A successful HTTP status code (200).

        Columns that are fully qualified in the query will be returned with
        a fully qualified name, for example, MyTable[MyColumn]. Columns
        that are renamed or created in the query will be returned within
        square bracket, for example, `[MyNewColumn]`.

        Parameters
        ----------
        `queries` : `str | list[str]`
            Query or list of queries to execute against the dataset.
        `impersonated_user_name` : `str`, optional
            The UPN of a user to be impersonated. If the model is not RLS
            enabled, this will be ignored.
        `include_nulls` : `bool`, optional
            Whether null (blank) values should be included in the result
            set. If unspecified, the default value is `false`.

        Returns
        -------
        `dict`
            Dict containing the results of the execution.
        """

        if isinstance(queries, str):
            qs = [{"query": queries}]
        else:
            qs = [{"query": query} for query in queries]

        dataset_execute_queries_request = {
            "queries": qs,
            "serializerSettings": {
                "includeNulls": include_nulls,
            },
            "impersonatedUserName": impersonated_user_name,
        }
        prepared_request = remove_no_values(dataset_execute_queries_request)

        resource = self.base_path + "/executeQueries"

        raw = self.post_raw(
            resource,
            self.session,
            payload=prepared_request,
        )

        return raw

    def parameters(
        self,
    ) -> list[dict]:
        """
        Return a list of parameters for the dataset.

        Returns
        -------
        `list[dict]`
            Parameter list.
        """

        resource = self.base_path + "/parameters"
        return self.get_raw(resource, self.session)

    def refresh(
        self,
        notify_option: str,
        apply_refresh_policy: bool = None,
        commit_mode: str = None,
        effective_date: str = None,
        max_parallelism: int = None,
        objects: list[dict] = None,
        retry_count: int = None,
        type: str = None,
    ) -> None:
        """
        Trigger a refresh of the dataset. An enhanced refresh is triggered
        only if a request option other than `notify_option` is set.

        Parameters
        ----------
        `notify_option` : `str`
            Mail notification options, e.g., "MailOnCompletion", "MailOnFailure",
            or "NoNotification".
        `apply_refresh_policy` : bool, optional
            Determine if the policy is applied or not.
        `commit_mode` : `str`, optional
            Determines if objects will be committed in batches or only when
            complete, e.g., "PartialBatch", or "Transactional".
        `effective_date` : `str`, optional
            If an incremental refresh policy is applied, the `effective_date`
            parameter overrides the current date.
        `max_parallelism` : `int`, optional
            The maximum number of threads on which to run parallel processing
            commands.
        `objects` : `list[dict]`, optional
            A list of objects to be processed, e.g.,

            ```
            [
                {
                "table": "Customer",
                "partition": "Robert"
                }
            ]
            ```

        `retry_count` : `int`, optional
            Number of times the operation will retry before failing.
        `type` : `str`, optional
           The type of processing to perform, e.g., "Automatic", "Calculate",
           "ClearValues", "DataOnly", "Defragment", or "Full".

        Notes
        -----
        See here for request options in greater detail:

        https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset#definitions
        """

        refresh_request = {
            "applyRefreshPolicy": apply_refresh_policy,
            "commitMode": commit_mode,
            "effectiveDate": effective_date,
            "maxParallelism": max_parallelism,
            "notifyOption": notify_option,
            "objects": objects,
            "retryCount": retry_count,
            "type": type,
        }

        prepared_request = remove_no_values(refresh_request)
        resource = self.base_path + "/refreshes"

        self.post(resource, self.session, prepared_request)

    def refresh_details(
        self,
        refresh_id: str,
    ) -> dict:
        """
        Returns execution details of an enhanced refresh operation for
        the dataset.

        Parameters
        ----------
        `refresh_id` : `str`
            Refresh Id to get the execution details for.

        Returns
        -------
        `dict`
            Refresh execution details.
        """

        resource = self.base_path + f"/refreshes/{refresh_id}"
        return self.get_raw(resource, self.session)

    def refresh_history(
        self,
        top: int = None,
    ) -> list[dict]:
        """
        Returns the refresh history for the dataset.

        Parameters
        ----------
        `top` : `int`, optional
            The requested number of entries in the refresh history. If
            not provided, the default is the last available 500 entries.

        Returns
        -------
        `list[dict]`
            List of refresh history entries.

        Raises
        ------
        `HTTPError`
            If the api response status code is not equal to 200.
        """
        # TODO: implement Refresh object

        resource = self.base_path + "/refreshes"
        params = {"$top": top}

        raw = self.get_raw(resource, self.session, params)

        return raw

    def refresh_schedule(
        self,
        direct_query=False,
    ) -> dict:
        """
        Return the Refresh Schedule or Direct Query Refresh Schedule for
        the dataset.

        Parameters
        ----------
        `direct_query` : `bool`, optional
            Return the Direct Query Refresh Schedule instead of the Refresh Schedule.

        Returns
        -------
        `dict`
            Refresh schedule or Direct Query Refresh Schedule.
        """

        if direct_query:
            resource = self.base_path + "/directQueryRefreshSchedule"
        else:
            resource = self.base_path + "/refreshSchedule"

        raw = self.get_raw(resource, self.session)

        return raw

    def take_over(
        self,
    ) -> None:
        """
        Transfer ownership of the dataset to the current authorized user.

        Raises
        ------
        `TypeError`
            If the dataset does not have a group_id. In other words, can't
            take over dataset in MyWorkspace, the authorized user already
            owns these.
        """

        if not self.group_id:
            raise TypeError(
                "Dataset does not have a group_id. Taking over a dataset can only be performed on a Dataset in a Group."
            )

        resource = self.base_path + "/Default.TakeOver"
        self.post(resource, self.session)

    def update(
        self,
        target_storage_mode: str,
    ) -> None:
        """
        Update the properties of the dataset.

        Parameters
        ----------
        `target_storage_mode` : `str`
            The dataset storage mode, .e.g, "PremiumFiles", or "Abf".
        """
        update_dataset_request = {"targetStorageMode": target_storage_mode}

        self.patch(self.base_path, self.session, update_dataset_request)

    def update_datasources(
        self,
        update_details: dict | list[dict],
    ) -> None:
        """
        Update the data sources of the dataset.

        Parameters
        ----------
        `update_details` : `dict | list[dict]`
            A dict, or list of dicts, representing the updates.

        Notes
        -----
        See here for how to construct the update details:

        https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/update-datasources#examples
        """

        if isinstance(update_details, dict):
            update_details_prepared = [update_details]
        else:
            update_details_prepared = update_details

        update_request = {"updateDetails": update_details_prepared}

        resource = self.base_path + "/Default.UpdateDatasources"
        self.post(resource, self.session, update_request)

    def update_user(
        self,
        identifier: str,
        principal_type: str,
        access_right: str,
    ) -> None:
        """
        Updates the existing permissions for a user of the dataset to the
        specified permissions.

        Parameters
        ----------
        `identifier` : `str`
            For principal type User, provide the UPN. Otherwise provide
            the object ID of the principal.
        `principal_type` : `str`
            The principal type, e.g., "App", "Group", "None", or "User".
        `access_right` : `str`
            The Dataset User Access Right to grant to the user, e.g.,"Read",
            "ReadExplore", "ReadReshare", or "ReadReshareExplore".
        """

        resource = self.base_path + "/users"
        dataset_user_access = {
            "identifier": identifier,
            "principalType": principal_type,
            "datasetUserAccessRight": access_right,
        }

        self.put(resource, self.session, dataset_user_access)

    def users(
        self,
    ) -> list[dict]:
        """
        Returns a list of principals that have access to the dataset.

        Returns
        -------
        `list[dict]`
            List of principals, e.g., Users, Groups, with access to the
            dataset.
        """

        resource = self.base_path + "/users"
        return self.get_raw(resource, self.session)
