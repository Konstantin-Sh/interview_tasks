import asyncio
import socket
import logging
from aiohttp import web
from logging.handlers import SysLogHandler
from request_checkers import is_vaild_tcp_upd_port, is_valid_ipv4_address, is_valid_ipv6_address


async def scan_port(event_loop, address, port):
    connect = asyncio.open_connection(address, port, loop=event_loop)
    try:
        await asyncio.wait_for(connect, timeout=10, loop=event_loop)
    except (asyncio.TimeoutError, ConnectionRefusedError):
        result = '{"port": "' + str(port) + '", "state": "close"}'
    except socket.error as msg:
        logging.error('port_scanner_srv: socket.error ' + msg)
        raise web.HTTPBadRequest(reason=msg)
    else:
        result = '{"port": "' + str(port) + '", "state": "open"}'
    finally:
        connect.close()
    return result


async def check_request(address, start_port, end_port):
    if not start_port.isdecimal() or not end_port.isdecimal():
        logging.error('port_scanner_srv: The start port or end port is not a number')
        raise web.HTTPBadRequest(reason='The start port or end port is not a number')
    start_port = int(start_port)
    end_port = int(end_port)
    if not (0 <= start_port <= 65535):
        logging.error('port_scanner_srv: The start port is out of range')
        raise web.HTTPBadRequest(reason='The start port is out of range')
    if not (0 <= end_port <= 65535):
        logging.error('port_scanner_srv: The end port is out of range')
        raise web.HTTPBadRequest(reason='The end port is out of range')


async def get_handler(request):
    address = request.match_info.get('address')
    start_port = request.match_info.get('start_port')
    end_port = request.match_info.get('end_port')
    await check_request(address, start_port, end_port)
    response = web.StreamResponse()
    response.headers['Content-Type'] = 'application/json'
    futures = [scan_port(event_loop, address, port)
               for port in range(int(start_port), int(end_port) + 1)]
    first_element = True
    for future in asyncio.as_completed(futures):
        result = await future
        if first_element:
            await response.prepare(request)
            await response.write(bytes('[' + result, encoding='utf8'))
            first_element = False
        else:
            await response.write(bytes(',' + result, encoding='utf8'))
    await response.write(bytes(']', encoding='utf-8'))
    await response.write_eof()
    return response


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    app = web.Application()
    app.router.add_get('/{address}/{start_port}/{end_port}', get_handler)
    logging.basicConfig(level=logging.DEBUG, handlers=[SysLogHandler(address='/dev/log'), SysLogHandler()])
    logging.info('port_scanner_srv: start')
    web.run_app(app, access_log_format='port_scanner_srv: %a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"')
    logging.info('port_scanner_srv: stop')
    event_loop.close()
