import discord
import asyncio
from utils.DBQuery import DBQuery
from utils import rankingHelpers

# ranks alphabetically
# purpose is to just show stats contained in db.

async def showStats(client, message):
  rankings = DBQuery.getRanking("faceit_id")
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    kills = int(player.get('kills') or 0)
    deaths = int(player.get('deaths') or 0)
    wins = int(player.get('wins') or 0)
    matches = int(player.get('matches') or 0)

    stats.append([
        player.get('nickname'),
        '%s/%s %s/%s' % (kills, deaths, wins, matches - wins)
    ])

  embed = await rankingHelpers.createRankEmbed(stats, 'Player stats', 'K/D W/L')
  await client.send_message(message.channel, embed=embed)
