import asyncio
import aiohttp

# 如果代理需要认证
# 同样在代理的前面加上用户名密码即可
# proxy = "http://username:password@127.0.0.1:7890"
proxy = 'http://127.0.0.1:7890'

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get', proxy=proxy) as r:
            print(await r.text())

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(main())
    asyncio.run(main())