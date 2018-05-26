import asyncio
from utils.Database import Database


db = Database()

class DBQuery:
  @staticmethod
  async def getPlayer(faceit_id):
    seq = (faceit_id)
    cmd = "SELECT * FROM players WHERE faceit_id = '%s';"
    return await db.contains(cmd, seq)

  @staticmethod
  async def insertPlayer(faceit_id, nickname, kills, deaths, wins, matches):
    seq = (faceit_id, nickname, kills, deaths, wins, matches)
    cmd = "INSERT INTO players (`faceit_id`, `nickname`, `kills`, `deaths`, `wins`, `matches`) VALUES ('%s', '%s', %s, %s, %s, %s);"
    await db.execute(cmd, seq)

  @staticmethod
  async def addToPlayer(faceit_id, kills, deaths, wins, matches):
    seq = (kills, deaths, wins, matches, faceit_id)
    cmd = "UPDATE players SET kills  = kills + %s, deaths = deaths + %s, wins = wins + %s, matches = matches + %s WHERE faceit_id = '%s';"
    await db.execute(cmd, seq)

  @staticmethod
  async def removePlayer(faceit_id):
    seq = (faceit_id)
    cmd = "DELETE FROM players WHERE faceit_id = '%s';"
    await db.execute(cmd, seq)

  @staticmethod
  async def getRanking(listOfCol, typeOfRanking):
    stringOfCol = listOfCol[0]

    for i in range(1, len(listOfCol)):
      stringOfCol += ', ' + listOfCol[i]
      
    seq = (stringOfCol, typeOfRanking)
    cmd = "SELECT %s FROM players ORDER BY %s DESC;"
    return await db.get(cmd, seq)