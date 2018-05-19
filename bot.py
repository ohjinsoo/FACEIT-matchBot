import discord
import aiohttp
import asyncio
import websockets
import json
import os

import getMatch
from models.Player import Player

FACEIT_URL = os.getenv('FACEIT_URL')
FACEIT_KEY = os.getenv('FACEIT_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
		print('Logged in as')
		print(client.user.name)
		print(client.user.id)

		# Start 60s timer to look for FACEIT matches.

		await getMatch.initRepeat(client)

def as_player(d):
	ret = Player()
	ret.__dict__.update(d)
	return ret


async def createStatsEmbed(player1):

	embed = discord.Embed(color=0xC9FFFF)
	embed.add_field(name='Level', value=player1.skill_level, inline=True)
	embed.add_field(name='ELO', value=player1.faceit_elo, inline=True)
	embed.add_field(name='Headshot %', value=player1.headshotPercentage + ' %', inline=True)
	embed.add_field(name='Matches Played', value=player1.matches, inline=True)
	embed.add_field(name='Win %', value=player1.winRate + ' %', inline=True)
	embed.add_field(name='AVG. K/D Ratio', value=player1.kdRatio, inline=True)
	embed.set_author(name=player1.nickname, icon_url=player1.avatar, url=player1.faceit_url)
	return embed

@client.event
async def on_message(message):
	if message.content.startswith('.stats '):
		player_nick = message.content[7:]
		faceitLink = FACEIT_URL + '/players?nickname=' + player_nick + '&game=csgo'

		print(faceitLink)

		headers = {"Authorization": FACEIT_KEY}
		async with aiohttp.ClientSession(headers=headers) as session:
			async with session.get(faceitLink) as requestForJson:
				dictOfPlayer = await requestForJson.json()

				# No permission to post or user does not exist.

				if requestForJson.status != 200:
					await client.send_message(message.channel, 'No such player found. (stats is case sensitive)')
					return

				if 'csgo' not in dictOfPlayer.get('games'):
					await client.send_message(message.channel, player_nick + ' has no stats for CSGO.')
					return

				# Only grab nickname, level, elo, and url as that is the only relevant variables.

				player1 = Player()
				player1.player_id = dictOfPlayer.get('player_id')
				player1.nickname = dictOfPlayer.get('nickname')
				player1.avatar = dictOfPlayer.get('avatar')
				player1.skill_level = dictOfPlayer.get('games').get('csgo').get('skill_level')
				player1.faceit_elo = dictOfPlayer.get('games').get('csgo').get('faceit_elo')
				player1.faceit_url = dictOfPlayer.get('faceit_url')[0:23] + "en/" + dictOfPlayer.get('faceit_url')[30:]

				faceitLink = FACEIT_URL + '/players/' + player1.player_id + '/stats/csgo'
				async with session.get(faceitLink) as requestForJson:
					dictOfPlayerStats = await requestForJson.json()

					if requestForJson.status != 200:
						await client.send_message(message.channel, player1.nickname + ' has no stats for CSGO.')
						return

					player1.headshotPercentage = dictOfPlayerStats.get('lifetime').get('Average Headshots %')
					player1.matches = dictOfPlayerStats.get('lifetime').get('Matches')
					player1.winRate = dictOfPlayerStats.get('lifetime').get('Win Rate %')
					player1.kdRatio = dictOfPlayerStats.get('lifetime').get('Average K/D Ratio')

					embed = await createStatsEmbed(player1)

					await client.send_message(message.channel, embed=embed)

client.run(BOT_TOKEN)
