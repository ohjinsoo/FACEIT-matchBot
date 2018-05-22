import discord
import aiohttp
import asyncio
import time
import json
import threading
import MySQLdb
from config import CHANNEL_ID
from models.Match import Match
from utils.Api import Api
from utils.DBQuery import DBQuery


# After getting match info about a new match, it will take a long time for FACEIT to have statistics ready.
# Because of this, whenever a match info is found, add it to 'addToDatabase' array.
# If array is not empty, ask FACEIT for statistics. If status != 200, do nothing.
# If status == 200, take all of the statistics from team members and update the MySQL database.

async def addMatchToDatabase(match, members):
  matchInfoRes = await Api.getMatchStats(match.matchId)

  if matchInfoRes.status != 200:
    return

  matchInfoResData = await matchInfoRes.json()

  teams = matchInfoResData.get('rounds')[1].get('teams')

  # if factionOne, team[0].
  # else,          team[1].
  players = teams[int(not match.isFactionOne)]

  for i in range(0, len(players)):
    player = players[i]
    playerName = player.get('nickname')
    isATrackedPlayer = False
    for j in range(0, len(members)):
      if playerName == members[j].get('nickname'):
        isATrackedPlayer = True

    if isATrackedPlayer:
      # Isn't actually a 'boolean' but rather count. But because the DB should only contain 0 or 1 copy
      # of a player, it acts as a boolean.
      existsInDB = await DBQuery.getPlayer(playerName)
      kills = player.get('player_stats').get('Kills')
      deaths = player.get('player_stats').get('Deaths')

      if existsInDB:
        player_id = player.get('player_id')
        insertPlayer(playerName, player_id, kills, deaths):

      else:
        addToPlayer(playerName, kills, deaths)

