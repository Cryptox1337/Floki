
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import asyncio
from models import *

import json
import os

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

response_string = {}
for i in os.listdir('./languages'):
	if i.endswith('.json'):
		with open(os.path.join('./languages', i)) as file:
			response = json.load(file)
		response_string[i.replace('.json',"")] = response


async def get_lang(guild, response):
	Guild_lang = await Guilds.filter(guild_id=guild.id).first()
	try:
		return response_string[Guild_lang.lang][response]
	except:
		return response_string['english'][response]

def setup(bot):
	bot.add_cog(Utils(bot))