import discord
import asyncio
from utils.DBQuery import DBQuery
from utils.DBQuery import DBQuery
from utils import rankingHelpers

# Sends a message that displays an embed with two fields:
# NAMES: { list of all the names }
# KDR: { player's kills:death ratio }

async def rankByWR(client, message):
  columnsNeeded = ['nickname', 'wins', 'matches']
  ranking = await DBQuery.getRanking(columnsNeeded, "wins")

  if ranking == ():
    await client.send_message(message.channel, 'There are no players in the Database.')
    return
    
  nicknameList = []
  winrateList = []
  for i in range(0, len(ranking)):

    # sorting alg (sorts by winrate, adds to nicknamelist as well):
    #   if winrateList is empty:
    #     append it
    #
    #   search through every value in winrateList.
    #     if wr > listvalue:
    #       insert in front of the listvalue
    #     else, if wr is smaller than every single value in the list:
    #       append it

    row = ranking[i]
    wr = float(row[1] / row[2])
    if len(winrateList) == 0:
      winrateList.append(wr)
      nicknameList.append(row[0])

    else:
      for j in range(0, len(winrateList)):
        if wr >= winrateList[j]:
          winrateList.insert(j, wr)
          nicknameList.insert(j, row[0])
          break
        elif winrateList[j] > wr and j == len(winrateList) - 1:
          winrateList.append(wr)
          nicknameList.append(row[0])
          break

  nicknameString = await rankingHelpers.parseList(nicknameList)
  winrateString = await rankingHelpers.parseFloatList(winrateList)

  embed = await rankingHelpers.createRankEmbed(nicknameString, winrateString, 'WINRATE')
  await client.send_message(message.channel, embed=embed)