
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import random

class Level(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):

		if not message.author.bot:
			user = await Users.filter(guild_id=message.guild.id, user_id=message.author.id).first()
			if user:
				_xp_table = await XP_Table.filter()
				xp = random.uniform(10.0, 25.0)
				user.xp += xp

				new_level = None
				for xp_table in _xp_table:
					if user.xp > xp_table.xp:
						new_level = xp_table.level
					else:
						break

				if new_level and not user.level >= new_level:
					user.level = new_level
					await message.channel.send(f"GG {message.author.mention}, you just advanced to level {new_level}")
				await user.save()

def setup(bot):
	bot.add_cog(Level(bot))