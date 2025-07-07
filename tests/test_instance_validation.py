import pytest

from scripts.core.models import Host


def test_instance_plain_integer_valid():
    """Test that plain integer instance values are valid."""
    host = Host(hostname="h1", environment="production", status="active", instance="1")
    assert host.instance == "1"


def test_instance_zero_valid():
    """Test that zero instance value is valid."""
    host = Host(hostname="h1", environment="production", status="active", instance="0")
    assert host.instance == "0"


@pytest.mark.parametrize("value", ["01", "1a", "1.0"])
def test_instance_plain_integer_invalid(value):
    """Test that non-plain integer instance values raise ValueError."""
    with pytest.raises(ValueError):
        Host(hostname="h1", environment="production", status="active", instance=value)
