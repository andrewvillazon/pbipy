import responses


@responses.activate
def test_get_groups(powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups",
        body="""
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
        """,
        content_type="application/json",
    )

    groups = powerbi.groups.get_groups()

    assert len(groups) == 3
    assert groups[2].name == "contoso"
    assert not groups[1].is_on_dedicated_capacity
    assert hasattr(groups[0], "name")
