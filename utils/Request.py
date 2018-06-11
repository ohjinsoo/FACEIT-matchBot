import aiohttp
import asyncio
from config import FACEIT_KEY, FACEIT_URL
from utils.Logger import log

class Request:
  client = aiohttp.ClientSession(headers={'Authorization': 'Bearer ' + FACEIT_KEY})

  def __init__(self):
    if self.client is None:
      self.client = aiohttp.ClientSession(headers={'Authorization': 'Bearer ' + FACEIT_KEY})

  async def get(self, url):
    log('req: %s' % url)

    try:
      body = self.client.get(FACEIT_URL + url)
      return await body
    except Exception as e:
      log("exception at Request.get(): " + str(e))
