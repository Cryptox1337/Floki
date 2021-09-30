import aiohttp
import traceback

from disnake.ext import commands, tasks
import disnake
import os


SLASH_COMMAND_GUILDS = (
	858852553545613322,
	415191587144859649,
)

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

	async def on_ready(self):
		print(f'Logged on as {self.user} (ID: {self.user.id})')
