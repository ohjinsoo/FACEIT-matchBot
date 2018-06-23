import asyncio
from config import TEAM_ID
from utils.Request import Request

request = Request()

class Api:
  @staticmethod
  async def getPlayer(nickname):
    return await request.get('/players?nickname=' + nickname + '&game=csgo')

  @staticmethod
  async def getPlayerStats(playerId):
    return await request.get('/players/' + playerId + '/stats/csgo')

  @staticmethod
  async def getTeamMembers():
    return await request.get('/teams/' + TEAM_ID)

  @staticmethod
  async def getPlayerMatch(playerId, rightBound):
    return await request.get('/players/' + playerId + '/history?game=csgo&from=' + str(rightBound) + '&offset=0&limit=1')

  @staticmethod
  async def getMatchInfo(gameId):
    return await request.get('/matches/' + gameId)

  @staticmethod
  async def getMatchStats(gameId):
    return await request.get('/matches/' + gameId + '/stats')
