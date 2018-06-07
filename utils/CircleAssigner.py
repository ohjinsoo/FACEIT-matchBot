import asyncio
from random import shuffle

async def createCirclesList():
  circles = ['🔴', '🔵', '⚪', '⚫', '⭕']
  #shuffle(circles)

  return circles

# assigns a circle for each player so that party members will have matching circles.

async def assignCircles(players):
  parties = {}
  circles = await createCirclesList()
  increment = -1
  for i in range(0, len(players)):
    increment = increment + 1

    player = players[i]
    if parties.get(player.party_id) is not None and player.party_id is not None:
      players[i].circle = parties[player.party_id]
      continue
    
    parties[player.party_id] = circles[increment]
    players[i].circle = circles[increment]

  return players