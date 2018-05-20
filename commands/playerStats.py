import asyncio
import discord

from models.Player import Player
from utils.Api import Api

async def stats(client, message):
  nickname = message.content[7:]
  playerRes = await Api.getPlayer(nickname)

  # No permission to post or user does not exist.
  if playerRes.status != 200:
    await client.send_message(message.channel, 'No such player found. (stats is case sensitive)')
    return

  playerResData = await playerRes.json()

  playerData = {
    'player_id': playerResData.get('player_id'),
    'nickname': playerResData.get('nickname'),
    'avatar': playerResData.get('avatar'),
    'faceit_url': playerResData.get('faceit_url')[0:23] + "en/" + playerResData.get('faceit_url')[30:],
  }

  if 'csgo' not in playerResData.get('games'):
    await client.send_message(message.channel, playerData['nickname'] + ' has no stats for CSGO.')
    return

  playerData.update({
    'skill_level': playerResData.get('games').get('csgo').get('skill_level'),
    'faceit_elo': playerResData.get('games').get('csgo').get('faceit_elo'),
  })

  playerStatsRes = await Api.getPlayerStats(playerData['player_id'])

  if playerStatsRes.status != 200:
    await client.send_message(message.channel, playerData['nickname'] + ' has no stats for CSGO.')
    return

  playerStatsResData = await playerStatsRes.json()

  playerData.update({
    'headshotPercentage': playerStatsResData.get('lifetime').get('Average Headshots %'),
    'matches': playerStatsResData.get('lifetime').get('Matches'),
    'winRate': playerStatsResData.get('lifetime').get('Win Rate %'),
    'kdRatio': playerStatsResData.get('lifetime').get('Average K/D Ratio'),
  })

  player = Player()
  player.__dict__.update(playerData)

  embed = await createStatsEmbed(player)

  await client.send_message(message.channel, embed=embed)

async def createStatsEmbed(player):
	embed = discord.Embed(color=0xC9FFFF)
	embed.set_author(name=player.nickname,
	                 icon_url=player.avatar, url=player.faceit_url)

	fields = {
		'Level': player.skill_level,
		'ELO': player.faceit_elo,
		'Headshot %': player.headshotPercentage + ' %',
		'Matches Played': player.matches,
		'Win %': player.winRate,
		'AVG. K/D Ratio': player.kdRatio,
	}

	for name, value in fields.items():
		embed.add_field(name=name, value=value, inline=True)

	return embed
