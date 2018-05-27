import discord
import asyncio
from utils.DBQuery import DBQuery
from utils import rankingHelpers

# Sends a message that displays an embed with two fields:
# NAMES: { list of all the names }
# KILS: { amount of kills each player has }

async def rankByWins(client, message):
  ranking = await DBQuery.getRanking(['nickname', 'wins'], 'wins')

  if ranking == ():
    await client.send_message(message.channel, 'There are no players in the Database.')
    return
    
  nicknameList = []
  winsList = []
  for i in range(0, len(ranking)):
    row = ranking[i]
    nicknameList.append(row[0])
    winsList.append(row[1])

  nicknameString = await rankingHelpers.parseList(nicknameList)
  winsString = await rankingHelpers.parseList(winsList)

  embed = await rankingHelpers.createRankEmbed(nicknameString, winsString, 'WINS')
  await client.send_message(message.channel, embed=embed)