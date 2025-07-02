from scripts.core.models import Host
import pytest


def test_instance_plain_integer_valid():
    host = Host(hostname="h1", environment="production", status="active", instance="1")
    assert host.instance == "1"


@pytest.mark.parametrize("value", ["01", "1a", "0", "1.0"])
def test_instance_plain_integer_invalid(value):
    with pytest.raises(ValueError):
        Host(hostname="h1", environment="production", status="active", instance=value)

