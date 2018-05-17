import discord
import aiohttp
import asyncio
import websockets
import json
import os

import getMatch 
from models.Player import Player


client = discord.Client()

@client.event
async def on_ready():
		print('Logged in as')
		print(client.user.name)
		print(client.user.id)

		# Start 60s timer to look for FACEIT matches.

		await getMatch.repeat(client)

def as_player(d):
	ret = Player()
	ret.__dict__.update(d)
	return ret

@client.event
async def on_message(message):
	if message.content.startswith('.stats '):
		player_nick = message.content[7:]
		faceitLink = os.environ['FACEIT_URL'] + '/players?nickname=' + player_nick

		headers={"Authorization": os.environ['FACEIT_KEY']}
		async with aiohttp.ClientSession(headers=headers) as session:
			async with session.get(faceitLink) as requestForJson:

				# requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
				dictOfPlayer = await requestForJson.json()

				# No permission to post or user does not exist.

				if requestForJson.status != 200:
					await client.send_message(message.channel, 'No such player found.')
					return

				# Only grab nickname, level, elo, and url as that is the only relevant variables.

				my_dict = {}
				my_dict['nickname'] = dictOfPlayer.get('nickname')
				my_dict['skill_level'] = dictOfPlayer.get('games').get('csgo').get('skill_level')
				my_dict['faceit_elo'] = dictOfPlayer.get('games').get('csgo').get('faceit_elo')
				my_dict['faceit_url'] = dictOfPlayer.get('faceit_url')[0:23] + "en/" + dictOfPlayer.get('faceit_url')[30:]

				# Create Player class using the dictionary.

				player1 = Player(json.dumps(my_dict))
				await client.send_message(message.channel, 'Player: ' + player1.nickname + "\nLevel: " + str(player1.skill_level) + "\nElo: "
																	+ str(player1.faceit_elo)  + "\nURL: " + player1.faceit_url)

client.run(os.environ['BOT_TOKEN'])
