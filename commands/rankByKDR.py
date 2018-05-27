import discord
import asyncio
from utils.DBQuery import DBQuery
from utils.DBQuery import DBQuery
from utils import rankingHelpers

async def rankByKDR(client, message):
  rankings = DBQuery.getRanking('kills/deaths')
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    kills = int(player.get('kills') or 0)
    deaths = int(player.get('deaths') or 0)

    stats.append([
      player.get('nickname'),
      '∞' if deaths == 0 else (kills / deaths)
    ])

  embed = await rankingHelpers.createRankEmbed(stats, 'Ranking by KDR', 'KDR')
  await client.send_message(message.channel, embed=embed)
