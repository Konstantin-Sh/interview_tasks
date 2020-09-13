import pytest
import sys
sys.path.append('../')
sys.path.append('.')
from port_scanner_srv import *


async def test_ya_ru_80(aiohttp_client):
    test_app = web.Application()
    test_app.router.add_get('/{address}/{start_port}/{end_port}', get_handler)
    client = await aiohttp_client(test_app)
    resp = await client.get('/ya.ru/80/80')
    assert resp.status == 200
    text = await resp.text()
    assert '[{"port": 80, "state": "open"}]' in text
