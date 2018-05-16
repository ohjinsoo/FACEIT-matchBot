import requests
import time
import json
import os
import threading

def printMatches(playersInGame, gameIds):
	for i in range(0, len(playersInGame)):
		currGameId = gameIds[i]
		currPlayers.append(playersInGame[i])
		for j in range(i + 1, len(playersInGame)):
			if currGameId == gameIds[j]:
				currPlayers.append(playersInGame[j])
				del gameIds[j]
				del playersInGame[j]
				j = j - 1

		faceitLink = os.environ['FACEIT_URL'] + '/matches/' + currGameId + '/stats'
		requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
		dictOfGame = requestForJson.json()

		client.send_message(message.channel, dictOfGame.get('rounds').get('round_stats').get('Score'))


def searchForAllMatches(players):
	playersInGame = []
	gameIds = []

	for i in range(0, len(players)):
		player = players[i]
		
		faceitLink = os.environ['FACEIT_URL'] + '/players/' + player['user_id'] + '/history?game=csgo&from=' + str(rightBound) + '&offset=0&limit=1'
		requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
		dictOfGames = requestForJson.json()

		if len(dictOfGames.get('items')) != 0:
			gameId = dictOfGames.get('items')[0].get('match_id')
			playersInGame.append(player['user_id'])
			gameIds.append(gameId)


	printMatches(playersInGame, gameIds)


faceitLink = os.environ['FACEIT_URL'] + '/teams/' + os.environ['TEAM_ID']
requestForJson = requests.get(faceitLink, headers={"Authorization": os.environ['FACEIT_KEY']})
dictOfPlayer = requestForJson.json()
members = dictOfPlayer.get('members')

rightBound = int(time.time())

def repeat():
  threading.Timer(60.0, repeat).start()
  searchForAllMatches(members)

repeat()