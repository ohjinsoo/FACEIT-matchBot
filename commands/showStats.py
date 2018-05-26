import discord
import asyncio
from utils.DBQuery import DBQuery
from utils import rankingHelpers

# ranks alphabetically
# purpose is to just show stats contained in db.

async def showStats(client, message):
  columnsNeeded = ['nickname', 'kills', 'deaths', 'wins', 'matches']
  ranking = await DBQuery.getRanking(columnsNeeded, "nickname")

  nicknameList = []
  killsList = []
  deathsList = []

  winsList = []
  matchesList = []

  for i in range(0, len(ranking)):
    row = ranking[i]
    nicknameList.append(row[0])
    killsList.append(row[1])
    deathsList.append(row[2])
    winsList.append(row[3])
    matchesList.append(row[4])

  nicknameString = await rankingHelpers.parseList(nicknameList)
  killsString = await rankingHelpers.parseList(killsList)
  deathsString = await rankingHelpers.parseList(deathsList)

  winsString = await rankingHelpers.parseList(winsList)
  matchesString = await rankingHelpers.parseList(matchesList)


  valuesList = [killsString, deathsString, nicknameString, winsString, matchesString]
  typeList = ['KILLS', 'DEATHS', '----------------', 'WINS', 'MATCHES']
  embedKD = await rankingHelpers.createEmbed(nicknameString, valuesList, typeList)

  msg = await client.send_message(message.channel, '\u200b')
  await client.edit_message(message=msg, embed=embedKD)
