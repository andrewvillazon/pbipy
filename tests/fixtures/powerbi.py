import pytest

from pbipy.powerbi import PowerBI


@pytest.fixture
def powerbi():
    return PowerBI("ABC123")
