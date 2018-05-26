from config import BOT_TOKEN

import discord
import asyncio
import websockets

from match.matchInfo import startMatchSearch
from commands.playerStats import stats
from commands.showTrackedPlayers import showPlayers
from commands.rankByKills import rankByKills
from commands.rankByKDR import rankByKDR
from commands.showStats import showStats
from utils.DBQuery import DBQuery


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as: %s [%s]' % (client.user.name, client.user.id))

    # Start 60s timer to look for FACEIT matches.
    await startMatchSearch(client)

@client.event
async def on_message(message):
    if message.content == '.commands':
        commands = '``` List of Commands: '
        commands += '\n    .stats [player]'
        commands += '\n    .players'
        commands += '\n    .players [stats]'
        commands += '\n    .ranks [kills/kdr]```'
        await client.send_message(message.channel, commands)

    elif message.content.startswith('.stats '):
        await stats(client, message)

    elif message.content == '.players':
        await showPlayers(client, message)

    elif message.content == '.ranks kills':
        await rankByKills(client, message)

    elif message.content == '.ranks kdr':
        await rankByKDR(client, message)

    elif message.content == '.players stats':
        await showStats(client, message)

client.run(BOT_TOKEN)
