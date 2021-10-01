
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *

class Config_Set(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command()
	async def set(self, inter):
		pass

def setup(bot):
	bot.add_cog(Config_Set(bot))