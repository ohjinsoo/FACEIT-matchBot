import discord
import asyncio

FACEIT_STEAM_ICON = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/e7/e74d4f1f7730b917c5a33c492a1112973862bb47_full.jpg'

async def createRankQuote(data, label = ''):
  stats = ''
  if label != '':
    stats = label + '\n'

    stats = 'PLAYERS       |  ' + stats

    stats += '------------------'

    for i in range(0, len(label)):
      stats += '-'

    stats += '\n'

  for i in range(0, len(data)):
    player = data[i]
    stats += '{:14}'.format(player[0]) + '|  '
    stats += str(player[1]) + '\n'

  return '```' + stats + '```'

async def sortByAvgKills(rankings):
  for i in range(0, len(rankings)):
    kills = int(rankings[i].get('kills') or 0)
    deaths = int(rankings[i].get('deaths') or 0)
    matches = int(rankings[i].get('matches') or 0)

    if matches != 0:
      rankings[i]['kills'] = float(kills / matches)
      rankings[i]['deaths'] = float(deaths / matches)

  ret = sorted(rankings, key=lambda k: k['kills'], reverse=True)


  return ret