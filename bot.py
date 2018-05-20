from config import BOT_TOKEN

import discord
import aiohttp
import asyncio
import websockets
import json

import getMatch
from models.Player import Player
from commands.stats import stats

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as: %s [%s]' % (client.user.name, client.user.id))

    # Start 60s timer to look for FACEIT matches.
    await getMatch.initRepeat(client)

def as_player(d):
    ret = Player()
    ret.__dict__.update(d)
    return ret

@client.event
async def on_message(message):
    if message.content.startswith('.stats '):
        await stats(client, message)

client.run(BOT_TOKEN)
