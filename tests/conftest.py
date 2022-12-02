import pytest

from pbipy.powerbi import PowerBI

from .fixtures.responsebodies import *
from .fixtures.models import *


@pytest.fixture
def powerbi():
    return PowerBI("ABC123")

