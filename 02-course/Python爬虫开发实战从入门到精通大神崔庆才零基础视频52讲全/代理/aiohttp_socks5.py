import asyncio
import aiohttp
# pip install aiohttp_socks
from aiohttp_socks import ProxyConnector, ProxyType

async def main():

    # # http
    # connector = ProxyConnector.from_url('http://127.0.0.1:7890')
    # # connector = ProxyConnector(
    # #     proxy_type=ProxyType.HTTP,
    # #     host='127.0.0.1',
    # #     port=7890,
    # #     # rdns=True
    # # )

    # # http+auth
    # connector = ProxyConnector.from_url('http://username:password@127.0.0.1:7890')
    # # connector = ProxyConnector(
    # #     proxy_type=ProxyType.HTTP,
    # #     host='127.0.0.1',
    # #     port=7890,
    # #     # username='user',
    # #     # password='password',
    # #     # rdns=True
    # # )

    # socks5
    # connector = ProxyConnector.from_url('socks5://127.0.0.1:7890')
    connector = ProxyConnector(
        proxy_type=ProxyType.SOCKS5,
        host='127.0.0.1',
        port=7890,
        # rdns=True
    )
    
    # # socks5+auth
    # connector = ProxyConnector.from_url('socks5://username:password@127.0.0.1:7890')
    # # connector = ProxyConnector(
    # #     proxy_type=ProxyType.SOCKS5,
    # #     host='127.0.0.1',
    # #     port=7890,
    # #     # username='user',
    # #     # password='password',
    # #     # rdns=True
    # # )

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get('https://httpbin.org/get') as r:
            print(await r.text())

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(main())
    asyncio.run(main())



