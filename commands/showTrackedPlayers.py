import asyncio
import discord

from models.Player import Player
from utils.Api import Api

async def showPlayers(client, message):
  teamRes = await Api.getTeamMembers()
  teamResData = await teamRes.json()

  teamName = teamResData.get('name')
  teamAvatar = teamResData.get('avatar')
  teamUrl = teamResData.get('faceit_url')[0:23] + "en/" + teamResData.get('faceit_url')[30:]
  teamMembers = teamResData.get('members')

  field = {}
  for i in range(0, len(teamMembers)):
    member = teamMembers[i]
    url = member.get('faceit_url')[0:23] + "en/" + member.get('faceit_url')[30:]
    field.update({
      member.get('nickname') : url
    })

  embed = discord.Embed(color=0XFF00FF)
  for name, value in field.items():
    embed.add_field(name=name, value=value, inline=True)

  embed.set_author(name=teamName,
                   icon_url=teamAvatar, url=teamUrl)

  await client.send_message(message.channel, embed=embed)