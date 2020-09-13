import pytest
from aiohttp.test_utils import setup_test_loop, RawTestServer, unused_port
import sys
sys.path.append('../')
sys.path.append('.')
from port_scanner_srv import *


@pytest.fixture(scope='module')
def create_loop():
    setup_test_loop()


async def test_handle_error():
    with pytest.raises(web.HTTPBadRequest):
        await handle_error('test')


async def test_scan_port_close():
    loop = asyncio.get_event_loop()
    result = await scan_port(loop, '127.1', 0)
    assert result == '{"port": 0, "state": "close"}'


async def test_scan_port_open():
    port = unused_port()
    loop = asyncio.get_event_loop()
    webserver = RawTestServer(lambda request: web.Response(), host='127.1', port=port)
    await webserver.start_server(loop=loop)
    result = await scan_port(loop, '127.1', port)
    assert result == '{"port": %s, "state": "open"}' % port


async def test_scan_port_exception():
    loop = asyncio.get_event_loop()
    with pytest.raises(web.HTTPBadRequest):
        await scan_port(loop, '127.0', 0)


@pytest.mark.parametrize(
    ('address', 'result'), [
        ('127.1', '127.1'),
        ('::1', '::1'),
        ('localhost', '127.0.0.1'),
    ]
)
async def test_resolve_and_check_address(address, result):
    loop = asyncio.get_event_loop()
    assert await resolve_and_check_address(loop, address) == result


async def test_resolve_and_check_address_exception():
    loop = asyncio.get_event_loop()
    with pytest.raises(web.HTTPBadRequest):
        await resolve_and_check_address(loop, 'a1ng9Ae1hah4Es3Aa1ki4Oop1eshFe')


@pytest.mark.parametrize(
    ('start_port', 'end_port'), [
        ('10000', '1'),
        ('bla-bla', '1000'),
        ('1000', 'bla-bla'),
        ('65536', '1000'),
        ('-1', '1000'),
        ('1000', '65536'),
        ('1000', '-1'),
    ]
)
async def test_check_ports(start_port, end_port):
    asyncio.get_event_loop()
    with pytest.raises(web.HTTPBadRequest):
        await check_ports(start_port, end_port)


async def test_get_handler_localhost_0(aiohttp_client):
    test_app = web.Application()
    test_app.router.add_get('/{address}/{start_port}/{end_port}', get_handler)
    client = await aiohttp_client(test_app)
    resp = await client.get('/localhost/0/0')
    assert resp.status == 200
    text = await resp.text()
    assert '[{"port": 0, "state": "close"}]' == text


async def test_get_handler_localhost_2_4(aiohttp_client):
    test_app = web.Application()
    test_app.router.add_get('/{address}/{start_port}/{end_port}', get_handler)
    client = await aiohttp_client(test_app)
    resp = await client.get('/localhost/2/4')
    assert resp.status == 200
    text = await resp.text()
    assert '{"port": 2, "state": "close"}' in text
    assert '{"port": 3, "state": "close"}' in text
    assert '{"port": 4, "state": "close"}' in text
    assert '[{"port": ' == text[0:10]
    assert ', "state": "close"},{"port": ' == text[11:40]
    assert ', "state": "close"},{"port": ' == text[41:70]
    assert ', "state": "close"}]' == text[71:]


async def test_get_handler_localhost_open(aiohttp_client):
    port = unused_port()
    loop = asyncio.get_event_loop()
    webserver = RawTestServer(lambda request: web.Response(), host='127.1', port=port)
    await webserver.start_server(loop=loop)
    test_app = web.Application()
    test_app.router.add_get('/{address}/{start_port}/{end_port}', get_handler)
    client = await aiohttp_client(test_app)
    resp = await client.get(f'/localhost/{port}/{port}')
    assert resp.status == 200
    text = await resp.text()
    assert text == '[{"port": %s, "state": "open"}]' % port
