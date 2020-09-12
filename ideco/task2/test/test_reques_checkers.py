import pytest
import sys
sys.path.append('../')
from request_checkers import (is_valid_tcp_upd_port,
                              is_valid_ipv4_address,
                              is_valid_ipv6_address)


@pytest.mark.parametrize(
    ('port', 'result'), [
        (65534, True),
        (65535, True),
        (65536, False),
        (-1, False),
        (0, True),
        (1, True),
    ]
)
def test_is_valid_tcp_upd_port(port, result):
    assert is_valid_tcp_upd_port(port) == result


@pytest.mark.parametrize(
('address', 'result'), [
        ('127.0.0.1', True),
        ('127.1', True),
        ('300.0.0.1', False),
        ('192.168.O.1', False),
        ('localhost', False),
    ]
)
def test_is_valid_ipv4_address(address, result):
    assert is_valid_ipv4_address(address) == result


# source http://www.ronnutter.com/ipv6-cheatsheet-on-identifying-valid-ipv6-addresses/
@pytest.mark.parametrize(
    ('address', 'result'), [
        ('::1', True),
        ('1200:0000:AB00:1235:0000:2552:7777:1313', True),
        ('1200::AB00:1234::2552:7778:1313', False),
        ('2001:db8:0:2', False),
        ('2001::db8:0:2', True),
        ('21DA:D3:0:2F3C:2AA:FF:EE28:9C5A', True),
        ('200:0000:AB00:1234:O000:2552:7778:1313', False),
    ]
)
def test_is_valid_ipv6_address(address, result):
    assert is_valid_ipv6_address(address) == result
