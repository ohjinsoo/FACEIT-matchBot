import discord
import asyncio
from utils.DBQuery import DBQuery
from utils.DBQuery import DBQuery
from utils import rankingHelpers

# Sends a message that displays an embed with two fields:
# NAMES: { list of all the names }
# KILS: { amount of kills each player has }

async def rankByKills(client, message):
  ranking = await DBQuery.killsRanking()
  nicknameList = []
  killsList = []
  for i in range(0, len(ranking)):
    row = ranking[i]
    nicknameList.append(row[0])
    killsList.append(row[1])

  nicknameString = await rankingHelpers.parseList(nicknameList)
  killsString = await rankingHelpers.parseList(killsList)

  embed = await rankingHelpers.createRankEmbed(nicknameString, killsString, 'KILLS')
  await client.send_message(message.channel, embed=embed)