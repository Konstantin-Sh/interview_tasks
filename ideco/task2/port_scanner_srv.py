import asyncio
import socket
import logging
import aiodns
from aiohttp import web
from logging.handlers import SysLogHandler
from request_checkers import (is_valid_tcp_upd_port,
                              is_valid_ipv4_address,
                              is_valid_ipv6_address)


async def handle_error(msg):
    logging.error('port_scanner_srv: ' + msg)
    raise web.HTTPBadRequest(reason=msg)


async def scan_port(address, port):
    connect = asyncio.open_connection(address, port, loop=event_loop)
    try:
        await asyncio.wait_for(connect, timeout=10, loop=event_loop)
    except (asyncio.TimeoutError, ConnectionRefusedError):
        result = '{"port": ' + str(port) + ', "state": "close"}'
    except socket.error as msg:
        await handle_error('socket.error ' + msg)
    else:
        result = '{"port": ' + str(port) + ', "state": "open"}'
    finally:
        connect.close()
    return result


async def is_valid_host(address):
    check_ip4 = is_valid_ipv4_address(address)
    check_ip6 = is_valid_ipv6_address(address)
    resolver = aiodns.DNSResolver(loop=event_loop)
    try:
        await resolver.gethostbyname(address, socket.AF_INET)
    except aiodns.error.DNSError:
        check_dns = False
    else:
        check_dns = True
    return check_ip4 or check_ip6 or check_dns


async def check_request(address, start_port, end_port):
    if not start_port.isdecimal() or not end_port.isdecimal():
        await handle_error('The start port or end port is not a number.')
    if not is_valid_tcp_upd_port(int(start_port)):
        await handle_error('The start port is out of range.')
    if not is_valid_tcp_upd_port(int(end_port)):
        await handle_error('The end port is out of range.')
    if start_port > end_port:
        await handle_error('The start port is larger than the end port.')
    if not await is_valid_host(address):
        await handle_error('The address or hostname wrong.')


async def get_handler(request):
    address = request.match_info.get('address')
    start_port = request.match_info.get('start_port')
    end_port = request.match_info.get('end_port')
    await check_request(address, start_port, end_port)
    response = web.StreamResponse()
    response.headers['Content-Type'] = 'application/json'
    futures = [scan_port(address, port)
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
# Debug environment
    event_loop.set_debug(True)
    logging.basicConfig(level=logging.DEBUG)
# End debug environment
    # logging.basicConfig(level=logging.INFO, handlers=[SysLogHandler(address='/dev/log'), SysLogHandler()])
    logging.info('port_scanner_srv: start')
    web.run_app(app, access_log_format='port_scanner_srv: %a %t "%r" %s %b'
                                       ' "%{Referer}i" "%{User-Agent}i"')
    logging.info('port_scanner_srv: stop')
    event_loop.close()
