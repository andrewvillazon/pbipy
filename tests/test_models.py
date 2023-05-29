from datetime import datetime


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
