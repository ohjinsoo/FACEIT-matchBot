import discord
import asyncio
import requests
import time
import json
import os
import threading

async def createEmbed(dictOfGame, currPlayers):
    winningFaction = dictOfGame.get('results').get('winner')
    isFactionOne = False
    factionOneList = dictOfGame.get('teams').get('faction1').get('roster_v1')
    for i in range(0, len(factionOneList)):
        factionOneMember = factionOneList[i].get('nickname')
        if factionOneMember == currPlayers[0]:
            isFactionOne = True
            break

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
        message += ' suck ROFL'


    embed = discord.Embed(title=outcome, description=message, color=0x00ff00)

    return embed


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
        requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
        print(requestForJson.json())
        if requestForJson.status_code == 404:
            return

        dictOfGame = requestForJson.json()
        embed = await createEmbed(dictOfGame, currPlayers)
        await client.send_message(discord.Object(id='445775038373691395'), embed=embed)

    rightBound = int(time.time())
    await asyncio.sleep(60)
    await repeat(client)


async def searchForAllMatches(players, client):
    playersInGame = []
    gameIds = []

    for i in range(0, len(players)):
        player = players[i]
        faceitLink = os.environ['FACEIT_URL'] + '/players/' + player['user_id'] + '/history?game=csgo&from=' + str(rightBound) + '&offset=0&limit=1'
        requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
        dictOfGames = requestForJson.json()

        if len(dictOfGames.get('items')) != 0:
            gameId = dictOfGames.get('items')[0].get('match_id')
            playersInGame.append(player['nickname'])
            gameIds.append(gameId)

    await printMatches(playersInGame, gameIds, client)

faceitLink = os.environ['FACEIT_URL'] + '/teams/' + os.environ['TEAM_ID']
requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
dictOfPlayer = requestForJson.json()
members = dictOfPlayer.get('members')
rightBound = int(time.time()) - 10000

async def repeat(c):
    client = c
    print(rightBound)
    await searchForAllMatches(members, client)

