import discord
import asyncio
from utils.DBQuery import DBQuery
from utils import rankingHelpers

async def rankByWins(client, message):
  rankings = DBQuery.getRanking('wins')
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    wins = int(player.get('wins') or 0)
    stats.append([player.get('nickname'), wins])

  embed = await rankingHelpers.createRankEmbed(stats, 'Ranking by wins', 'Wins')
  await client.send_message(message.channel, embed=embed)
