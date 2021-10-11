
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *

import json
import os
from datetime import datetime
import pytz

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

async def getIsUserBanned(guild, check_user):
	for ban_entry in await guild.bans():
		if ban_entry.user.id == check_user.id:
			return True

	return False

async def getNowUTCDate():
	date = datetime.fromtimestamp(int(datetime.utcnow().timestamp()))

	return date


async def getEndUTCDate(duration):
	end_date = datetime.fromtimestamp(int(datetime.utcnow().timestamp()) + int(duration))

	return end_date


async def getDuration(end_date):
	now_stamp = int(datetime.utcnow().timestamp())
	end_stamp = int(datetime.strptime(str(end_date), "%Y-%m-%d %H:%M:%S%z").strftime("%s"))
	duration = end_stamp - now_stamp

	return duration


async def convertTimeZone(guild, time):
	server = await Guilds.get(guild_id=guild.id)
	if server:
		new_timezone = pytz.timezone(server.timezone)
		new_time = time.astimezone(new_timezone)

	return new_time


async def getResponseChannel(guild, response_type):
	response_channel = None
	response = await Response_Channels.filter(guild_id=guild.id, response_type=response_type).first()
	if response:
		if response.status == "enabled":
			try:
				response_channel = guild.get_channel(response.channel_id)
			except:
				pass

	return response_channel


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