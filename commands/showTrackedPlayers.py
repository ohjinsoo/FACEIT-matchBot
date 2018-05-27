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

  memberList = ''

  for i in range(0, len(teamMembers)):
    member = teamMembers[i]
    memberList += member.get('faceit_url')[0:23] + "en/" + member.get('faceit_url')[30:]
    memberList += '\n'

  embed = discord.Embed(color=0XFF00FF)
  embed.add_field(name='List of all players in ' + teamName, value=memberList, inline=True)

  embed.set_author(name=teamName,
                   icon_url=teamAvatar, url=teamUrl)

  await client.send_message(message.channel, embed=embed)
