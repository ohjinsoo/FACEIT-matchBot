import discord
import aiohttp
import asyncio
import time
import json
import threading
import MySQLdb
import gc
from match.matchStats import addMatchToDatabase
from config import CHANNEL_ID_1, CHANNEL_ID_2, ENV, SLEEP_LENGTH
from models.Match import Match
from models.Player import Player
from utils.Api import Api
from utils.DBQuery import DBQuery
from utils.CircleAssigner import assignCircles
from utils.Logger import log

addToDatabase = []
FACEIT_STEAM_ICON = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/e7/e74d4f1f7730b917c5a33c492a1112973862bb47_full.jpg'

# Initialize the bounds for when to start searching for matches.
# If user, make it the current time.
# If dev, make it a day before (for testing purposes!)

rightBound = int(time.time()) 

if (ENV == 'dev'):
  rightBound -= 86400

# Parses through the list and adds a new line in between each one.

async def parsePlayerList(playerList):
  ret = ''

  for i in range(0, len(playerList)):
    ret += playerList[i].circle + ' ' + playerList[i].nickname + '\n'

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
  # color = red
  color = 0xff0000

  # If winner, make embed green.
  if (match.isFactionOne and match.winner == 'faction1') or (not match.isFactionOne and match.winner == 'faction2'):
    color = 0x00ff00

  startTime = time.strftime('%B %d,  %I:%M %p', time.localtime(match.start))
  endTime = time.strftime('%B %d,  %I:%M %p', time.localtime(match.end))

  match.factionOne = await assignCircles(match.factionOne)
  match.factionTwo = await assignCircles(match.factionTwo)

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
                   icon_url=FACEIT_STEAM_ICON,url=match.matchUrl)

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
    if matchRes.status != 200:
      return

    matchResData = await matchRes.json()
    serverAndMap = matchResData.get('voting')
    server = ''
    mapName = ''
    if type(serverAndMap) is list:
      server = serverAndMap[0].get('location').get('name')
      mapName = serverAndMap[0].get('map').get('name')

    else:
      server = serverAndMap.get('location').get('pick')[0]
      mapName = serverAndMap.get('map').get('pick')[0]

    factionOne = matchResData.get('teams').get('faction1')
    factionTwo = matchResData.get('teams').get('faction2')

    factionOneList = factionOne.get('roster_v1')
    factionTwoList = factionTwo.get('roster_v1')

    if factionOneList == None:
      factionOneList = factionOne.get('roster')
      factionTwoList = factionTwo.get('roster')

    currentTime = time.strftime('%B %d,  %I:%M %p', time.localtime(time.time()))
    print(currentTime + '::: ' + mapName + ' at ' + server)

    factionOneMembers = []
    factionTwoMembers = []
    isFactionOne = False

    # Made two separate for loops just incase it is a match with uneven teams (for whatever reason)

    for i in range(0, len(factionOneList)):
      player = Player()
      player.nickname = factionOneList[i].get('nickname')
      player.party_id = factionOneList[i].get('active_team_id')
      factionOneMembers.append(player)

      if player.nickname == playersInGame[0]:
        isFactionOne = True

    for i in range(0, len(factionTwoList)):
      player = Player()
      player.nickname = factionTwoList[i].get('nickname')
      player.party_id = factionTwoList[i].get('active_team_id')
      factionTwoMembers.append(player)

    matchData = {
      'matchId' : matchResData.get('match_id'),
      'matchUrl' : matchResData.get('faceit_url')[0:23] + "en/" + matchResData.get('faceit_url')[30:],

      'server': server,
      'mapName' : mapName,

      'start' : matchResData.get('started_at'),
      'end' : matchResData.get('finished_at'),

      'winner' : matchResData.get('results').get('winner'),

      'factionOneName' : factionOne.get('name'),
      'factionTwoName' : factionTwo.get('name'),

      'factionOne' : factionOneMembers,
      'factionTwo' : factionTwoMembers,
      'isFactionOne' : isFactionOne
    }

    match = Match()
    match.__dict__.update(matchData)

    global addToDatabase
    addToDatabase.append(match)
    embed = await createMatchEmbed(match, currPlayers)

    outcome = '**' + currPlayers[0] + '**'
    for i in range(1, len(currPlayers)):
      outcome += ', **' + currPlayers[i] + '**'

    # if embed == green, add ' won!' , else add ' lost :('

    if (match.winner == 'faction1' and match.isFactionOne) or (match.winner == 'faction2' and not match.isFactionOne):
      outcome += ' won their match!'
    else:
      outcome += ' lost their match :('

    message = await client.send_message(discord.Object(id=CHANNEL_ID_1), outcome)
    await client.edit_message(message=message, embed=embed)

    if CHANNEL_ID_2 != 'null':
      message = await client.send_message(discord.Object(id=CHANNEL_ID_2), outcome)
      await client.edit_message(message=message, embed=embed)

    # Update the rightBound of match searches.
    global rightBound
    rightBound = int(time.time())

# Search each of the team members if there is a game that finished
# between the current time and the time when the bot first logged on.
# (bot login time will update each time there is a match found)

async def searchForAllMatches(players, client):
  playersInGame = []
  gameIds = []

  if players is None:
    return

  for i in range(0, len(players)):
    player = players[i]
    
    global rightBound
    matchRes = await Api.getPlayerMatch(player['user_id'], rightBound)

    if matchRes.status != 200:
      continue

    matchResData = await matchRes.json()
    match = matchResData.get('items')

    if len(match) != 0:
      playersInGame.append(player['nickname'])
      gameIds.append(match[0].get('match_id'))

  if len(playersInGame) != 0:
    await printMatches(playersInGame, gameIds, client)


async def startMatchSearch(client):
  teamRes = await Api.getTeamMembers()
  teamResData = await teamRes.json()
  members = teamResData.get('members')

  log('startMatchSearch w/ ' + str(members))

  for i in range(0, len(members)):
    member = members[i]
    DBQuery.insertOrUpdate(member.get('user_id'), member.get('nickname'))

  await matchSearch(client, members)


async def matchSearch(client, members):
  await searchForAllMatches(members, client)
  global addToDatabase
  if len(addToDatabase) != 0:
    for i in range(0, len(addToDatabase)):
      await addMatchToDatabase(addToDatabase[i], members)

    addToDatabase = []

  await asyncio.sleep(SLEEP_LENGTH)
  gc.collect()
  await matchSearch(client, members)

