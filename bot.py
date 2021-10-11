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
			await Guilds.get_or_create(guild_id=guild.id)
			for user in guild.members:
				await Users.get_or_create(guild_id=guild.id, user_id=user.id)

			for channel in guild.channels:
				await Channels.get_or_create(guild_id=guild.id, channel_id=channel.id)

			for role in guild.roles:
				if not role.managed and not role.name == "@everyone":
					await Roles.get_or_create(guild_id=guild.id, role_id=role.id)


			await check_role_and_channels(guild)

		print(f'Logged on as {self.user} (ID: {self.user.id})')

async def check_role_and_channels(guild):
	channels = await Channels.filter(guild_id=guild.id)
	roles = await Roles.filter(guild_id=guild.id)

	for channel in channels:
		_channel = guild.get_channel(channel.channel_id)

		if not _channel:
			await channel.delete()

	for role in roles:
		_role = disnake.utils.get(guild.roles, id=role.role_id)

		if not _role:
			await role.delete()