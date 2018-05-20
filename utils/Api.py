import asyncio
from utils.Request import Request

request = Request()

class Api:
  @staticmethod
  async def getPlayer(nickname):
    return await request.get('/players?nickname=' + nickname + '&game=csgo')

  @staticmethod
  async def getPlayerStats(playerId):
    return await request.get('/players/' + playerId + '/stats/csgo')

