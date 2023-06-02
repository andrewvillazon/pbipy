from datetime import datetime

from pbipy.models import DatasetRefreshDetail, Gateway


def test_refresh_post_init_parses_dates(refresh_from_raw):
    assert isinstance(refresh_from_raw.start_time, datetime)
    assert isinstance(refresh_from_raw.end_time, datetime)


def test_group_creation_from_raw(group_from_raw):
    assert hasattr(group_from_raw, "id")
    assert hasattr(group_from_raw, "is_on_dedicated_capacity")
    assert hasattr(group_from_raw, "is_read_only")
    assert hasattr(group_from_raw, "name")


def test_group_creation(group):
    assert group.id == "3d9b93c6-7b6d-4801-a491-1738910904fd"
    assert group.name == "marketing group"
    assert not group.is_on_dedicated_capacity
    assert not group.is_read_only
    assert not group.type


def test_dataset_creation_from_raw(dataset_from_raw):
    assert hasattr(dataset_from_raw, "id")
    assert hasattr(dataset_from_raw, "name")
    assert hasattr(dataset_from_raw, "add_rows_api_enabled")
    assert hasattr(dataset_from_raw, "is_refreshable")


def test_dataset_post_init_parses_dates(dataset_from_raw):
    assert isinstance(dataset_from_raw.created_date, datetime)


def test_app_creation(app_from_raw):
    assert hasattr(app_from_raw, "id")
    assert hasattr(app_from_raw, "description")
    assert hasattr(app_from_raw, "name")
    assert hasattr(app_from_raw, "published_by")
    assert hasattr(app_from_raw, "last_update")

    assert isinstance(app_from_raw.last_update, datetime)
    assert app_from_raw.id == "3d9b93c6-7b6d-4801-a491-1738910904fd"
    assert app_from_raw.description == "The marketing app"

def test_report_creation(report_from_raw):
    assert hasattr(report_from_raw, "app_id")
    assert hasattr(report_from_raw, "dataset_id")
    assert hasattr(report_from_raw, "id")
    assert hasattr(report_from_raw, "name")
    assert hasattr(report_from_raw, "description")
    assert hasattr(report_from_raw, "is_owned_by_me")
    assert hasattr(report_from_raw, "web_url")
    assert hasattr(report_from_raw, "embed_url")
    assert hasattr(report_from_raw, "users")
    assert hasattr(report_from_raw, "subscriptions")

    assert report_from_raw.is_owned_by_me
    assert report_from_raw.app_id == "3d9b93c6-7b6d-4801-a491-1738910904fd"
    assert isinstance(report_from_raw.users, list)
    assert not report_from_raw.report_type
    assert not report_from_raw.subscriptions


def test_dashboard_creation(dashboard_from_raw):
    assert hasattr(dashboard_from_raw, "id")
    assert hasattr(dashboard_from_raw, "display_name")
    assert hasattr(dashboard_from_raw, "is_read_only")
    assert hasattr(dashboard_from_raw, "web_url")
    assert hasattr(dashboard_from_raw, "app_id")
    assert hasattr(dashboard_from_raw, "embed_url")
    assert hasattr(dashboard_from_raw, "users")
    assert hasattr(dashboard_from_raw, "subscriptions")

    assert not dashboard_from_raw.is_read_only
    assert dashboard_from_raw.display_name == "SalesMarketing"
    assert dashboard_from_raw.app_id == "3d9b93c6-7b6d-4801-a491-1738910904fd"
    assert dashboard_from_raw.id == "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac"


def test_tile_creation(tile_from_raw):
    assert hasattr(tile_from_raw, "col_span")
    assert hasattr(tile_from_raw, "dataset_id")
    assert hasattr(tile_from_raw, "embed_data")
    assert hasattr(tile_from_raw, "embed_url")
    assert hasattr(tile_from_raw, "id")
    assert hasattr(tile_from_raw, "report_id")
    assert hasattr(tile_from_raw, "row_span")
    assert hasattr(tile_from_raw, "title")
    assert hasattr(tile_from_raw, "sub_title")


def test_gateway_creation(gateway_from_raw):
    assert hasattr(gateway_from_raw, "id")
    assert hasattr(gateway_from_raw, "gateway_id")
    assert hasattr(gateway_from_raw, "gateway_annotation")
    assert hasattr(gateway_from_raw, "gateway_status")
    assert hasattr(gateway_from_raw, "name")
    assert hasattr(gateway_from_raw, "public_key")
    assert hasattr(gateway_from_raw, "type")

    assert isinstance(gateway_from_raw, Gateway)
    assert gateway_from_raw.id == "1f69e798-5852-4fdd-ab01-33bb14b6e934"
    assert gateway_from_raw.type == "Resource"
    assert gateway_from_raw.name == "My_Sample_Gateway"
    assert isinstance(gateway_from_raw.public_key, dict)


def test_dataset_refresh_detail_status_code_200_creation(dataset_refresh_detail_200_status_code_from_raw):
    assert isinstance(dataset_refresh_detail_200_status_code_from_raw, DatasetRefreshDetail)
    
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "start_time")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "end_time")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "type")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "commit_mode")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "status")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "extended_status")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "current_refresh_type")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "number_of_attempts")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "messages")
    assert hasattr(dataset_refresh_detail_200_status_code_from_raw, "objects")

    assert isinstance(dataset_refresh_detail_200_status_code_from_raw.start_time, datetime)
    assert isinstance(dataset_refresh_detail_200_status_code_from_raw.end_time, datetime)
    assert isinstance(dataset_refresh_detail_200_status_code_from_raw.objects, list)

    assert len(dataset_refresh_detail_200_status_code_from_raw.objects) == 18
    assert dataset_refresh_detail_200_status_code_from_raw.messages is None


def test_dataset_refresh_detail_status_code_202_creation(dataset_refresh_detail_202_status_code_from_raw):
    assert isinstance(dataset_refresh_detail_202_status_code_from_raw, DatasetRefreshDetail)
    
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "start_time")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "end_time")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "type")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "commit_mode")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "status")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "extended_status")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "current_refresh_type")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "number_of_attempts")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "messages")
    assert hasattr(dataset_refresh_detail_202_status_code_from_raw, "objects")

    assert dataset_refresh_detail_202_status_code_from_raw.end_time is None
    assert dataset_refresh_detail_202_status_code_from_raw.objects is None