import discord
import asyncio
import websockets
import requests
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
		await getMatch.repeat(client)

def as_player(d):
	ret = Player()
	ret.__dict__.update(d)
	return ret

@client.event
async def on_message(message):
	if message.content.startswith('!hello'):
		testPlayers = ['jinsooerino', 'NotPAWEL']
		testGameRoom = '134d7306-3c5b-4433-a1fa-ede77825b2aa'

		faceitLink = os.environ['FACEIT_URL'] + '/matches/' + testGameRoom + '/stats'
		requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
		dictOfGame = requestForJson.json()

		embed = discord.Embed(title="team x vs. team y", description="-------------------------------------------------------------------------------------------------", color=0x00ff00)
		embed.add_field(name="Fiel1", value="hi", inline=False)
		embed.add_field(name="", value="-------------------------------------------------------------------------------------------------", inline=False)
		await client.send_message(client.get_channel('445775038373691395'), embed=embed)


	if message.content.startswith('.stats '):
		player_nick = message.content[7:]
		faceitLink = os.environ['FACEIT_URL'] + '/players?nickname=' + player_nick
		requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
		dictOfPlayer = requestForJson.json()

		if json.dumps(dictOfPlayer)[2:8] == 'errors':
			await client.send_message(message.channel, 'No such player found.')
			return

		my_dict = {}
		my_dict['nickname'] = dictOfPlayer.get('nickname')
		my_dict['skill_level'] = dictOfPlayer.get('games').get('csgo').get('skill_level')
		my_dict['faceit_elo'] = dictOfPlayer.get('games').get('csgo').get('faceit_elo')
		my_dict['faceit_url'] = dictOfPlayer.get('faceit_url')[0:23] + "en/" + dictOfPlayer.get('faceit_url')[30:]

		player1 = Player(json.dumps(my_dict))
		await client.send_message(message.channel, 'Player: ' + player1.nickname + "\nLevel: " + str(player1.skill_level) + "\nElo: "
																	+ str(player1.faceit_elo)  + "\nURL: " + player1.faceit_url)

client.run(os.environ['BOT_TOKEN'])
