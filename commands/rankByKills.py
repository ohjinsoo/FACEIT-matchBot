import discord
import asyncio
from utils.DBQuery import DBQuery
from utils import rankingHelpers

async def rankByKills(client, message):
  rankings = DBQuery.getRanking()
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    kills = int(player.get('kills') or 0)
    stats.append([player.get('nickname'), kills])

  embed = await rankingHelpers.createRankEmbed(stats, 'Ranking by kills', 'Kills')
  await client.send_message(message.channel, embed=embed)
