import discord
import aiohttp
import asyncio
import requests
import time
import json
import os
import threading

# Creates the embedded message to showcase a FACEIT match.

async def createEmbed(dictOfGame, currPlayers):
    winningFaction = dictOfGame.get('results').get('winner')
    isFactionOne = False
    factionOneList = dictOfGame.get('teams').get('faction1').get('roster_v1')
    for i in range(0, len(factionOneList)):
        factionOneMember = factionOneList[i].get('nickname')
        if factionOneMember == currPlayers[0]:
            isFactionOne = True
            break

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
        currGameId = gameIds[i]
        currPlayers = []
        currPlayers.append(playersInGame[i])
        for j in range(i + 1, len(playersInGame)):
            if currGameId == gameIds[j]:
                currPlayers.append(playersInGame[j])
                del gameIds[j]
                del playersInGame[j]
                j = j - 1


        faceitLink = os.environ['FACEIT_URL'] + '/matches/' + currGameId
        # requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
        headers={"Authorization": os.environ['FACEIT_KEY']}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(faceitLink) as requestForJson:
                if requestForJson.status == 404:
                    return

                dictOfGame = await requestForJson.json()
                embed = await createEmbed(dictOfGame, currPlayers)
                await client.send_message(discord.Object(id=os.environ['CHANNEL_ID']), embed=embed)

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

    for i in range(0, len(players)):
        player = players[i]
        faceitLink = os.environ['FACEIT_URL'] + '/players/' + player['user_id'] + '/history?game=csgo&from=' + str(rightBound) + '&offset=0&limit=1'
        # requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
        headers={"Authorization": os.environ['FACEIT_KEY']}
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

faceitLink = os.environ['FACEIT_URL'] + '/teams/' + os.environ['TEAM_ID']
requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
dictOfPlayer = requestForJson.json()
members = dictOfPlayer.get('members')
rightBound = int(time.time())

async def repeat(c):
    client = c
    print(rightBound)
    await searchForAllMatches(members, client)

