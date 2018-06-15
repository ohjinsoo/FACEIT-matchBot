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