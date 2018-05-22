import asyncio
from utils.Database import Database

db = Database()

class DBQuery:
  @staticmethod
  async def getPlayer(nickname):
    seq =(nickname)
    cmd = "SELECT * FROM Player WHERE nickname = '%s';"
    return await db.get(cmd, seq)

  @staticmethod
  async def insertPlayer(nickname, player_id, kills, deaths):
    seq = (nickname, player_id, kills, deaths)
    cmd = "INSERT INTO Player (`nickname`, `player_id`, `kills`, `deaths`) VALUES (%s, %s, %s, %s);"
    await db.execute(cmd, seq)

  @staticmethod
  async def addToPlayer(nickname, kills, deaths):
    seq = (kills, deaths, nickname)
    cmd = "UPDATE Player SET kills  = kills + %s, deaths = deaths + %s WHERE nickname = '%s';"
    await db.execute(cmd, seq)

  @staticmethod
  async def removePlayer(nickname):
    seq = (nickname)
    cmd = "DELETE FROM Player WHERE nickname = '%s';"
    await db.execute(cmd, seq)