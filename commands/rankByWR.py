import discord
import asyncio
from utils.DBQuery import DBQuery
from utils.DBQuery import DBQuery
from utils import rankingHelpers

async def rankByWR(client, message):
  rankings = DBQuery.getRanking('wins/matches')
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    wins = int(player.get('wins') or 0)
    matches = int(player.get('matches') or 0)

    stats.append([
        player.get('nickname'),
        '∞' if matches == 0 else (wins / matches)
    ])

  embed = await rankingHelpers.createRankEmbed(stats, 'Ranking by winrate', 'Winrate')
  await client.send_message(message.channel, embed=embed)
