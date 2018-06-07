from __future__ import division
import asyncio
from utils.DBQuery import DBQuery
from utils import rankingHelpers

async def playerRanking(client, message):
  print("playerRanking\n")
  data = {}

  command = message.content[7:]
  if command == 'kills':
    data = await orderByKills()
  elif command == 'kdr':
    data = await orderByKDR()
  elif command == 'wins':
    data = await orderByWins()
  elif command == 'wr':
    data = await orderByWR()
  else:
    data = await showPlayersStats()

  await embed(client, message, data)

async def embed(client, message, data):
  stats = data.get('stats')
  title = data.get('title')
  label = data.get('label')

  embed = await rankingHelpers.createRankEmbed(stats, title, label)
  await client.send_message(message.channel, embed=embed)

async def showPlayersStats():
  rankings = DBQuery.getRanking("faceit_id", "ASC")
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

  return {'stats': stats, 'title': 'Player stats', 'label': 'K/D W/L'}

async def orderByKills():
  rankings = DBQuery.getRanking()
  print(rankings)
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    kills = int(player.get('kills') or 0)
    stats.append([player.get('nickname'), kills])

  return {'stats': stats, 'title': 'Ranking by kills', 'label': 'Kills'}

async def orderByKDR():
  rankings = DBQuery.getRanking('kills/deaths')
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    kills = int(player.get('kills') or 0)
    deaths = int(player.get('deaths') or 0)

    stats.append([
      player.get('nickname'),
      '∞' if deaths == 0 else "%.2f" % (kills / deaths)
    ])

  return {'stats': stats, 'title': 'Ranking by KDR', 'label': 'KDR'}


async def orderByWins():
  rankings = DBQuery.getRanking('wins')
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    wins = int(player.get('wins') or 0)
    stats.append([player.get('nickname'), wins])

  return {'stats': stats, 'title': 'Ranking by wins', 'label': 'Wins'}


async def orderByWR():
  rankings = DBQuery.getRanking('wins/matches')
  stats = []

  for i in range(0, len(rankings)):
    player = rankings[i]
    wins = int(player.get('wins') or 0)
    matches = int(player.get('matches') or 0)

    stats.append([
        player.get('nickname'),
        '∞%' if matches == 0 else "%.2f" % (wins / matches * 100)
    ])

  return {'stats': stats, 'title': 'Ranking by winrate', 'label': 'Winrate'}
