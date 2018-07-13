import asyncio
import discord

from models.Player import Player
from utils.Api import Api
from match.matchInfo import printMatches
from match.matchStats import addMatchToDatabase
from utils.Logger import log

addedMatches = {}

async def record(client, message):
  matchID = message.content[8:]
  isAdmin = message.channel.permissions_for(message.author).administrator

  if not isAdmin or addedMatches.get(matchID):
    await client.send_message(message.channel, 'Error, match has already been added, or you are not an admin.')
    return

  teamRes = await Api.getTeamMembers()
  teamResData = await teamRes.json()
  members = teamResData.get('members')

  playersInGame = []
  gameIds = []

  matchInfoRes = await Api.getMatchInfo(matchID)
  matchInfoData = await matchInfoRes.json()
  teams = matchInfoData.get('teams')

  allMembers = {}

  if members is None or teams is None:
    await client.send_message(message.channel, 'Error, could not find match. Sorry!')
    return


  factionOne = matchInfoData.get('teams').get('faction1')
  factionTwo = matchInfoData.get('teams').get('faction2')

  factionOneList = factionOne.get('roster_v1')
  factionTwoList = factionTwo.get('roster_v1')

  if factionOneList == None:
    factionOneList = factionOne.get('roster')
    factionTwoList = factionTwo.get('roster')

  for i in range(0, len(factionOneList)):
    allMembers[factionOneList[i].get('nickname')] = True
    allMembers[factionTwoList[i].get('nickname')] = True;

  for i in range(0, len(members)):
    try:
      playerNick = members[i]['nickname'];
      if allMembers[playerNick]:
        playersInGame.append(playerNick)
        gameIds.append(matchID)
    except Exception as e:
      log('Exception! ' + str(e))
      continue

  if len(playersInGame) != 0:
    await printMatches(playersInGame, gameIds, client)

  addedMatches[matchID] = True
