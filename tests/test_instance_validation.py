import pytest

from scripts.core.models import Host


def test_instance_plain_integer_valid():
    host = Host(hostname="h1", environment="production", status="active", instance="1")
    assert host.instance == "1"


def test_instance_zero_valid():
    host = Host(hostname="h1", environment="production", status="active", instance="0")
    assert host.instance == "0"


@pytest.mark.parametrize("value", ["01", "1a", "1.0"])
def test_instance_plain_integer_invalid(value):
    with pytest.raises(ValueError):
        Host(hostname="h1", environment="production", status="active", instance=value)
