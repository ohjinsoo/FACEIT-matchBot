from config import BOT_TOKEN

import discord
import asyncio
import websockets

from match.matchInfo import startMatchSearch
from commands.playerStats import stats
from commands.showTrackedPlayers import showPlayers
from commands.playerRanking import playerRanking
from commands.recordMatch import record
from utils.DBQuery import DBQuery
from utils.Logger import log

client = discord.Client()

@client.event
async def on_ready():
    log('Logged in as: %s [%s]' % (client.user.name, client.user.id))

    # Start 60s timer to look for FACEIT matches.
    await startMatchSearch(client)

@client.event
async def on_message(message):
    if message.content == '.commands':
        commands = '``` List of Commands: [] - required, <> - optional'
        commands += '\n    .record [matchID]  <-  ADMIN COMMAND'
        commands += '\n    .stats [player]'
        commands += '\n    .players'
        commands += '\n    .ranks <kills/kdr/wins/winrate>```'
        await client.send_message(message.channel, commands)

    elif message.content.startswith('.stats '):
        await stats(client, message)

    elif message.content == '.players':
        await showPlayers(client, message)

    elif message.content.startswith('.record '):
        await record(client, message)

    elif message.content.startswith('.ranks'):
        await playerRanking(client, message)
client.run(BOT_TOKEN)
