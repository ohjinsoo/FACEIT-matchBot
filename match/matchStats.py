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

async def addMatchToDatabase(match):
  matchInfoRes = await Api.getMatchStats(match.matchId)

  if matchInfoRes.status != 200:
  	return

  
  
