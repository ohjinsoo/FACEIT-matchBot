import discord
import asyncio
from utils.DBQuery import DBQuery
from utils.DBQuery import DBQuery
from utils import rankingHelpers

# Sends a message that displays an embed with two fields:
# NAMES: { list of all the names }
# KDR: { player's kills:death ratio }

async def rankByKDR(client, message):
  columnsNeeded = ['nickname', 'kills', 'deaths']
  ranking = await DBQuery.getRanking(columnsNeeded, "kills")

  if ranking == ():
    await client.send_message(message.channel, 'There are no players in the Database.')
    return
  
  nicknameList = []
  kdrList = []
  for i in range(0, len(ranking)):

    # sorting alg (sorts by kdr, adds to nicknamelist as well):
    #   if kdrdList is empty:
    #     append it
    #
    #   search through every value in kdrList.
    #   if kdr > listvalue:
    #     insert in front of the listvalue
    #   else, if kdr is smaller than every single value in the list:
    #     append it

    row = ranking[i]
    kdr = float(row[1] / row[2])
    if len(kdrList) == 0:
      kdrList.append(kdr)
      nicknameList.append(row[0])

    else:
      for j in range(0, len(kdrList)):
        if kdr >= kdrList[j]:
          kdrList.insert(j, kdr)
          nicknameList.insert(j, row[0])
          break
        elif kdrList[j] > kdr and j == len(kdrList) - 1:
          kdrList.append(kdr)
          nicknameList.append(row[0])
          break

  nicknameString = await rankingHelpers.parseList(nicknameList)
  kdrString = await rankingHelpers.parseFloatList(kdrList)

  embed = await rankingHelpers.createRankEmbed(nicknameString, kdrString, 'KDR')
  await client.send_message(message.channel, embed=embed)