import discord
import aiohttp
import asyncio
import time
import json
import threading
import os

FACEIT_URL = os.getenv('FACEIT_URL')
FACEIT_KEY = os.getenv('FACEIT_KEY')
TEAM_ID = os.getenv('TEAM_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

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


async def createMatchEmbed(dictOfGame, currPlayers):
    gameUrl = dictOfGame.get('faceit_url')
    serverAndMap = dictOfGame.get('voting')

    server = serverAndMap[0].get('location').get('name')
    mapName = serverAndMap[0].get('map').get('name')

    # Times are in UNIX time.

    startTime = dictOfGame.get('started_at')
    endTime = dictOfGame.get('finished_at')


    winningFaction = dictOfGame.get('results').get('winner')
    isFactionOne = False

    # A list with everyone in factionOne and name of factionOne

    factionOneList = dictOfGame.get('teams').get('faction1').get('roster_v1')
    factionOneName = dictOfGame.get('teams').get('faction1').get('name')
    factionOneMembers = []
    for i in range(0, len(factionOneList)):
        factionOneMember = factionOneList[i].get('nickname')
        factionOneMembers.append(factionOneMember)

        # Check to see which faction is the team we are tracking is in.

        if factionOneMember == currPlayers[0]:
            isFactionOne = True

    # A list with everyone in factionTwo and name of factionTwo

    factionTwoList = dictOfGame.get('teams').get('faction2').get('roster_v1')
    factionTwoName = dictOfGame.get('teams').get('faction2').get('name')
    factionTwoMembers = []
    for i in range(0, len(factionTwoList)):
        factionTwoMember = factionTwoList[i].get('nickname')
        factionTwoMembers.append(factionTwoMember)

    color = 0x00ff00
    outcome = ''
    message = ''
    message += currPlayers[0]
    for i in range(1, len(currPlayers)):
        message += ', ' + currPlayers[i]

    # WIN CONDITIONS: They are faction one and winning faction is faction1, or they are faction two and winning faction is faction2

    if (isFactionOne and winningFaction == 'faction1') or (not isFactionOne and winningFaction == 'faction2'):
        outcome = 'WINNERS'
        message += ' won lul'
    else:
        outcome = "LOSERS"
        message += ' sucks ROFL'
        color = 0xff0000


    embed = discord.Embed(title=outcome, description=message, color=color)
    return embed

# Split the list into groups that have the gameIds in common. Each gameId is a different game, so each embedded message
# should have information on only one game.

async def printMatches(playersInGame, gameIds, client):
    for i in range(0, len(playersInGame)):
        if (i >= len(playersInGame)):
            break
        print('this is i ' + str(i))
        currGameId = gameIds[i]
        currPlayers = []
        currPlayers.append(playersInGame[i])
        j = i + 1
        while j < len(playersInGame):
            print('this is j ' + str(j))
            if currGameId == gameIds[j]:
                currPlayers.append(playersInGame[j])
                del gameIds[j]
                del playersInGame[j]
                j = j - 1
            j = j + 1


        faceitLink = FACEIT_URL + '/matches/' + currGameId
        headers={"Authorization": FACEIT_KEY}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(faceitLink) as requestForJson:
                if requestForJson.status == 404:
                    return

                dictOfGame = await requestForJson.json()
                embed = await createMatchEmbed(dictOfGame, currPlayers)
                await client.send_message(discord.Object(id=CHANNEL_ID), embed=embed)

    # Update the rightBound of match searches, wait 60s, and repeat.

    rightBound = int(time.time())
    await asyncio.sleep(60)
    await repeat(client)


# Search each of the team members if there is a game that finished
# between the current time and the time when the bot first logged on.
# (bot login time will update each time there is a match found)

async def searchForAllMatches(players, client):
    playersInGame = []
    gameIds = []

    print('players', players)

    for i in range(0, len(players)):
        player = players[i]
        faceitLink = FACEIT_URL + '/players/' + player['user_id'] + '/history?game=csgo&from=' + str(rightBound) + '&offset=0&limit=1'
        headers={"Authorization": FACEIT_KEY}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(faceitLink) as requestForJson:
                dictOfGames = await requestForJson.json()
                print(dictOfGames)
                if requestForJson.status == 200 and len(dictOfGames.get('items')) != 0:
                    gameId = dictOfGames.get('items')[0].get('match_id')
                    playersInGame.append(player['nickname'])
                    gameIds.append(gameId)

    await printMatches(playersInGame, gameIds, client)

# Gather all of the team member's names and initialize the rightBound of member searches.
# Requests is used here only because can't use 'async with aiohttp' as a global variable.


members = {}
rightBound = int(time.time())

# Initialize members here. Don't need to do it more than once as the teams should not change.
# If a member is added to the team, simply restart bot.
# (should we re-initialize teams every minute so you do't have to restart bot? Very rarely are teams changed, so I dunno)

async def initRepeat(c):
    client = c
    faceitLink = FACEIT_URL + '/teams/' + TEAM_ID
    headers={"Authorization": FACEIT_KEY}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(faceitLink) as requestForJson:
            dictOfPlayer = await requestForJson.json()
            members = dictOfPlayer.get('members')
            await searchForAllMatches(members, client)

async def repeat(c):
    client = c
    await searchForAllMatches(members, client)

