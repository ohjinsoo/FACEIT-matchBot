import discord
import asyncio

FACEIT_STEAM_ICON = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/e7/e74d4f1f7730b917c5a33c492a1112973862bb47_full.jpg'

async def createRankEmbed(nicknameString, valuesString, typeOfValue):
  listField = {
    'NAMES' :  nicknameString,
    '# OF ' + typeOfValue : valuesString
  }
  embed = discord.Embed(color=0xFFFFFF)
  embed.set_author(name= typeOfValue +" Leaderboard", icon_url=FACEIT_STEAM_ICON)
  for name, value in listField.items():
    embed.add_field(name=name, value=value, inline=True)

  return embed

async def parseList(list):
  ret = ''

  for i in range(0, len(list)):
    ret += str(list[i]) + '\n'

  return str(ret)