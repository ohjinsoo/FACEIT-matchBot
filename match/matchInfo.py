import discord
import aiohttp
import asyncio
import time
import json
import threading
import MySQLdb
from match.matchStats import addMatchToDatabase
from config import CHANNEL_ID
from models.Match import Match
from utils.Api import Api

async def parsePlayerList(playerList):
  ret = ''

  for i in range(0, len(playerList)):
    ret += playerList[i] + '\n'

  return str(ret)

# Creates the embedded message to showcase a FACEIT match.
# CURRENT INFO GATHERED FOR AN EMBEDDED MESSAGE (currently the same amount of information as ToyBot) :

#           - faceit url to the match page
#           - server location and map name
#           - faction name (ie, team_x and team_y)
#           - the start/end times
#           - which faction won/lost
#           - which faction the team we are tracking is in. (if won, msg will be green. if lost, msg will be red)
#           - the players in faction1
#           - the players in faction2

async def createMatchEmbed(match, currPlayers):

  isFactionOne = False
  factionOneList = match.factionOne

  for i in range(0, len(factionOneList)):
    if factionOneList[i] == currPlayers[0]:
      isFactionOne = True
      break

  # color = red
  color = 0xff0000

  # If winner, make embed green. 
  if (isFactionOne and match.winner == 'faction1') or (not isFactionOne and match.winner == 'faction2'):
    color = 0x00ff00

  startTime = time.strftime('%B %d,  %I:%M %p', time.localtime(match.start))
  endTime = time.strftime('%B %d,  %I:%M %p', time.localtime(match.end))

  matchFields = {

    match.factionOneName : await parsePlayerList(match.factionOne),
    match.factionTwoName : await parsePlayerList(match.factionTwo),

    'Map' : match.mapName,

    '\u200b' : '------------------------------------------------------------------------------',

    'Start Time: ': startTime,
    'End Time: ': endTime,
    'Server Location' : match.server
  }


  title = match.factionOneName + ' vs. ' + match.factionTwoName
  embed = discord.Embed(color=color, description='------------------------------------------------------------------------------')
  embed.set_author(name=title,
    # not sure what kind of icon i should put, so i put faceit icon from steam as a placeholder
                   icon_url='https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/e7/e74d4f1f7730b917c5a33c492a1112973862bb47_full.jpg',url=match.matchUrl)

  for name, value in matchFields.items():
    embed.add_field(name=name, value=value, inline=True)

  # Adds an empty field at the bottom to make the embed look cleaner
  embed.add_field(name='\u200b', value='\u200b', inline=False)
  embed.set_footer(text='\u200b')

  return embed


# Split the list into groups that have the gameIds in common. Each gameId is a different game, so each embedded message
# should have information on only one game.

async def printMatches(playersInGame, gameIds, client):
  for i in range(0, len(playersInGame)):
    if (i >= len(playersInGame)):
      break

    currGameId = gameIds[i]
    currPlayers = []
    currPlayers.append(playersInGame[i])

    j = i + 1
    while j < len(playersInGame):
      if currGameId == gameIds[j]:
        currPlayers.append(playersInGame[j])
        del gameIds[j]
        del playersInGame[j]
        j = j - 1
      j = j + 1


    matchRes = await Api.getMatchInfo(currGameId)
    if matchRes.status == 404:
      return

    matchResData = await matchRes.json()
    serverAndMap = matchResData.get('voting')

    factionOne = matchResData.get('teams').get('faction1')
    factionTwo = matchResData.get('teams').get('faction2')

    factionOneList = factionOne.get('roster_v1')
    factionTwoList = factionTwo.get('roster_v1')

    factionOneMembers = []
    factionTwoMembers = []

    # Made two separate for loops just incase it is a match with uneven teams (for whatever reason)

    for i in range(0, len(factionOneList)):
      mem = factionOneList[i].get('nickname')
      factionOneMembers.append(str(mem))

    for i in range(0, len(factionTwoList)):
      mem = factionTwoList[i].get('nickname')
      factionTwoMembers.append(str(mem))

    matchData = {
      'matchId' : matchResData.get('match_id'),
      'matchUrl' : matchResData.get('faceit_url')[0:23] + "en/" + matchResData.get('faceit_url')[30:],

      'server': serverAndMap[0].get('location').get('name'),
      'mapName' : serverAndMap[0].get('map').get('name'),
      'start' : matchResData.get('started_at'),
      'end' : matchResData.get('finished_at'),

      'winner' : matchResData.get('results').get('winner'),

      'factionOneName' : factionOne.get('name'),
      'factionTwoName' : factionTwo.get('name'),

      'factionOne' : factionOneMembers,
      'factionTwo' : factionTwoMembers
    }

    match = Match()
    match.__dict__.update(matchData)

    addToDatabase.append(match)
    embed = await createMatchEmbed(match, currPlayers)

    outcome = '**' + currPlayers[0] + '**'
    for i in range(1, len(currPlayers)):
      outcome += ', **' + currPlayers[i] + '**'

    # if embed == green, add ' won!' , else add ' lost :('
    if embed.color == 0x00ff00:
      outcome += ' won their match!'
    else:
      outcome += ' lost their match :('

    message = await client.send_message(discord.Object(id=CHANNEL_ID), outcome)
    await client.edit_message(message=message, embed=embed)



# Search each of the team members if there is a game that finished
# between the current time and the time when the bot first logged on.
# (bot login time will update each time there is a match found)

async def searchForAllMatches(players, client, rightBound):
  playersInGame = []
  gameIds = []

  print('players', players)

  if players is None:
    return

  for i in range(0, len(players)):
    player = players[i]
    matchRes = await Api.getPlayerMatch(player['user_id'], rightBound)
    matchResData = await matchRes.json()
    match = matchResData.get('items')

    if matchRes.status == 200 and len(match) != 0:
      playersInGame.append(player['nickname'])
      gameIds.append(match[0].get('match_id'))

  await printMatches(playersInGame, gameIds, client)


# Initialize members here. Don't need to do it more than once as the teams should not change.
# If a member is added to the team, simply restart bot.

async def startMatchSearch(client):
  teamRes = await Api.getTeamMembers()
  teamResData = await teamRes.json()
  members = teamResData.get('members')
  rightBound = int(time.time())
  await matchSearch(client, members, rightBound)


async def matchSearch(client, members, rightBound):
  await searchForAllMatches(members, client, rightBound)
  await asyncio.sleep(60)

  # Update the rightBound of match searches.
  rightBound = int(time.time())

  if len(addToDatabase) != 0:
    for i in range(0, len(addToDatabase)):
      await matchStats.addMatchToDatabase(addToDatabase[i])

  await matchSearch(client, members, rightBound)
  




addToDatabase = []

