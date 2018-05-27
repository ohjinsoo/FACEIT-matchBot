import discord
import asyncio

FACEIT_STEAM_ICON = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/e7/e74d4f1f7730b917c5a33c492a1112973862bb47_full.jpg'

async def createRankEmbed(data, title, label = ''):
  embed = discord.Embed(color=0xFFFFFF)
  embed.set_author(name=title, icon_url=FACEIT_STEAM_ICON)

  stats = ''

  for i in range(0, len(data)):
    player = data[i]
    stats += "%s\t%s\n" % (player[1], player[0])

  embed.add_field(name=label, value=stats, inline=True)

  return embed
