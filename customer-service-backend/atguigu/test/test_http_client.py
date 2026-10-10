import asyncio

from conf.config import settings
from infrastructure import http_util

async def test():
    http_util.init_http_client()
    result = await http_util.http_client.get(f"{settings.commerce_api_base_url}/user/u1001/orders")
    print(result.json())

if __name__ == '__main__':
    asyncio.run(test())