from config import BOT_TOKEN

import discord
import aiohttp
import asyncio
import websockets
import json

from match import matchStats
from models.Player import Player
from commands.playerStats import stats

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as: %s [%s]' % (client.user.name, client.user.id))

    # Start 60s timer to look for FACEIT matches.
    await matchStats.startMatchSearch(client)

@client.event
async def on_message(message):
    if message.content.startswith('.stats '):
        await stats(client, message)

client.run(BOT_TOKEN)
