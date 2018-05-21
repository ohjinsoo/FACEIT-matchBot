import asyncio
import discord

from models.Player import Player
from utils.Api import Api

async def showPlayers(client, message):
  teamRes = await Api.getTeamMembers()
  teamResData = await teamRes.json()
  members = teamResData.get('members')