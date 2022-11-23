"""
Module contains Python representations of Power BI objects.

The powerbi.PowerBI() client will attempt to translate API responses into instances 
of these objects.
"""

from dataclasses import dataclass, field
from typing import Optional

from dateutil.parser import parse

from .utils import camel_case_dict_keys


@dataclass(kw_only=True)
class PBIObject:
    raw: dict = field(repr=False, default=None)

    @classmethod
    def from_raw(cls, raw):
        """
        Create an instance of a `PBIObject` from the raw json response
        of an API Endpoint.

        Parameters
        ----------
        `raw` : `dict`
            Raw json response from the API call.

        Returns
        -------
        `PBIObject`
            Instance of a `PBIObject` type. The type returned depends on
            where it was called from.
        """

        kwargs = camel_case_dict_keys(raw)
        return cls(**kwargs, raw=raw)


@dataclass
class Group(PBIObject):
    """A Power BI group. Commonly called a Workspace."""

    id: str
    
    name: str = None
    type: str = None
    is_read_only: bool = None
    is_on_dedicated_capacity: bool = None
    capacity_id: str = None
    dataflow_storage_id: str = None


@dataclass
class Dataset(PBIObject):
    """A Power BI Dataset."""

    id: str
    
    name: str = None
    web_url: str = None
    add_rows_api_enabled: bool = None
    is_refreshable: bool = None
    is_effective_identity_required: bool = None
    is_effective_identity_roles_required: bool = None
    is_in_place_sharing_enabled: bool = None
    is_on_prem_gateway_required: bool = None
    target_storage_mode: str = None
    created_date: str = None
    create_report_embed_url: str = None
    qna_embed_url: str = None
    upstream_datasets: str = None
    users: Optional[list] = field(default_factory=list)
    configured_by: str = None

    def __post_init__(self):
        if self.created_date:
            self.created_date = parse(self.created_date)


@dataclass
class Refresh(PBIObject):
    """A Power BI refresh history entry."""
    
    id: int = None
    
    request_id: str = None
    refresh_type: str = None
    start_time: str = None
    end_time: str = None
    status: str = None
    service_exception_json: str = None

    def __post_init__(self):
        if self.start_time:
            self.start_time = parse(self.start_time)
        if self.end_time:
            self.end_time = parse(self.end_time)


# TODO: Consider creating subclassess for each subtype.
@dataclass
class ActivityEvent(PBIObject):
    """Power BI Auditing Events.
    
    Activity Events are audit and tracked activity on the Power BI 
    instance. Examples of Activity Events can include: viewing reports, 
    refreshing datasets, updating apps, etc.

    While there are many types of Activity Events, pybi consolidates these 
    into an `ActivityEvent` object. Attributes not related to an activity 
    type will be set to `None`.
    """
    
    id: str
    
    activity: str = None
    activity_id: str = None
    app_dashboard_id: str = None
    app_id: str = None
    app_name: str = None
    app_report_id: str = None
    artifact_id: str = None
    artifact_kind: str = None
    artifact_name: str = None
    client_ip: str = None
    consumption_method: str = None
    creation_time: str = None
    dashboard_id: str = None
    dashboard_name: str = None
    data_connectivity_mode: str = None
    dataflow_access_token_request_parameters: str = None
    dataflow_id: str = None
    dataflow_name: str = None
    dataflow_type: str = None
    dataset_id: str = None
    dataset_name: str = None
    datasets: str = None
    datasource_object_ids: str = None
    distribution_method: str = None
    exported_artifact_info: str = None
    folder_access_requests: str = None
    folder_display_name: str = None
    folder_object_id: str = None
    gateway_id: str = None
    has_full_report_attachment: bool = None
    import_display_name: str = None
    import_id: str = None
    import_source: str = None
    import_type: str = None
    is_success: bool = None
    item_name: str = None
    last_refresh_time: str = None
    model_id: str = None
    models_snapshots: str = None
    monikers: str = None
    object_id: str = None
    operation: str = None
    org_app_permission: str = None
    organization_id: str = None
    record_type: str = None
    refresh_type: str = None
    report_id: str = None
    report_name: str = None
    report_type: int = None
    request_id: str = None
    schedules: str = None
    share_link_id: str = None
    sharing_action: str = None
    sharing_information: str = None
    user_agent: str = None
    user_id: str = None
    user_key: str = None
    user_type: int = None
    work_space_name: str = None
    workload: str = None
    workspace_id: str = None

    def __post_init__(self):
        if self.creation_time:
            self.creation_time = parse(self.creation_time)
        if self.last_refresh_time:
            self.last_refresh_time = parse(self.last_refresh_time)
