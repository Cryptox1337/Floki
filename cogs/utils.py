
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import asyncio
from models import *

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot


def setup(bot):
	bot.add_cog(Utils(bot))