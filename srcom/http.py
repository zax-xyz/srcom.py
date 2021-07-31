import sys

import aiohttp


class HTTPClient:

    BASE = "https://www.speedrun.com/api/v1/"

    def __init__(self):
        user_agent = "srcom.py Python/{}.{}.{} aiohttp/{}".format(
            *sys.version_info[:3],
            aiohttp.__version__,
        )
        self.session = aiohttp.ClientSession(headers={"User-Agent": user_agent})

    async def _get(self, url, params=None):
        async with self.session.get(url, params=params) as resp:
            return await resp.json()

    async def get(self, path, params=None):
        url = self.BASE + path
        return await self._get(url, params)

    async def close(self):
        await self.session.close()
