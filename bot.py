from disnake.ext import commands, tasks
import disnake
import os
from tortoise import Tortoise
import config
from models import *


SLASH_COMMAND_GUILDS = (
	893584194633097227,
	893584194633097227,
)

async def init_db():
	await Tortoise.init(config=config.TORTOISE_ORM)

class Floki(commands.Bot):
	def __init__(self, **kwargs):
		super().__init__(
			command_prefix=commands.when_mentioned_or('?'),
			intents=disnake.Intents.all(),
			test_guilds=SLASH_COMMAND_GUILDS,
			**kwargs
		)

		self.startup = disnake.utils.utcnow()

		for filename in os.listdir("cogs"):
			if filename.endswith(".py"):
				self.load_extension(f"cogs.{filename[:-3]}")

		self.loop.run_until_complete(init_db())		

	async def on_ready(self):
		for guild in self.guilds:
			server, created = await Guilds.get_or_create(guild_id=guild.id)
			for user in guild.members:
				server, created = await Users.get_or_create(guild_id=guild.id, user_id=user.id)

			for channel in guild.channels:
				await Channels.get_or_create(guild_id=guild.id, channel_id=channel.id)	


		print(f'Logged on as {self.user} (ID: {self.user.id})')



