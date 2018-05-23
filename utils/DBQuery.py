import asyncio
from config import DB_TABLE_NAME
from utils.Database import Database


db = Database()

class DBQuery:
  @staticmethod
  async def getPlayer(nickname):
    seq = (nickname)
    cmd = "SELECT * FROM " + DB_TABLE_NAME + " WHERE nickname = '%s';"
    return await db.get(cmd, nickname)

  @staticmethod
  async def insertPlayer(nickname, player_id, kills, deaths, wins, matches):
    seq = (nickname, kills, deaths, wins, matches)
    cmd = "INSERT INTO " + DB_TABLE_NAME + " (`nickname`, `kills`, `deaths`, `wins`, `matches`) VALUES ('%s', %s, %s, %s, %s);"
    await db.execute(cmd, seq)

  @staticmethod
  async def addToPlayer(nickname, kills, deaths, wins, matches):
    seq = (kills, deaths, wins, matches, nickname)
    cmd = "UPDATE " + DB_TABLE_NAME + " SET kills  = kills + %s, deaths = deaths + %s, wins = wins + %s, matches = matches + %s WHERE nickname = '%s';"
    await db.execute(cmd, seq)

  @staticmethod
  async def removePlayer(nickname):
    seq = (nickname)
    cmd = "DELETE FROM " + DB_TABLE_NAME + " WHERE nickname = '%s';"
    await db.execute(cmd, seq)