import asyncio
from utils.Database import Database

db = Database()

class DBQuery:
  @staticmethod
  async def getPlayer(nickname):
    cmd = "SELECT * FROM Player WHERE nickname = '%s';" % (nickname)
    return await db.get(cmd)

  @staticmethod
  async def insertPlayer(nickname, player_id, kills, deaths):
    cmd = "INSERT INTO Player (`nickname`, `player_id`, `kills`, `deaths`) VALUES ('%s', %s, %s, %s);" % (nickname, player_id, kills, deaths)
    await db.execute(cmd)

  @staticmethod
  async def addToPlayer(nickname, kills, deaths):
    cmd = "UPDATE Player SET kills  = kills + %s, deaths = deaths + %s WHERE nickname = '%s';" % (kills, deaths, nickname)
    await db.execute(cmd)

  @staticmethod
  async def removePlayer(nickname):
    cmd = "DELETE FROM Player WHERE nickname = '%s';" % (nickname)
    await db.execute(cmd)