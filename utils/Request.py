import aiohttp
import asyncio
from config import FACEIT_KEY, FACEIT_URL
from utils.Logger import log

class Request:
  client = aiohttp.ClientSession(headers={'Authorization': 'Bearer ' + FACEIT_KEY})

  async def get(self, url):
    log('req: %s' % url)

    body = await self.client.get(FACEIT_URL + url)
    try:
      log('Rate Limit Left: ' + body.headers['X-Ratelimit-Remaining-Hour'])
    except:
      log('Cant find rate limit, heres the body: ' + str(body))
    return body