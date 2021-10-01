
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

	@set.sub_command(name = 'language')
	async def set_language(
		self,
		inter: disnake.ApplicationCommandInteraction,
		language = commands.param(
			choices = [
				disnake.OptionChoice('English', 'english'),
				disnake.OptionChoice('German', 'german')
			]
		)
	):
		guild = await Guilds.get(guild_id=inter.guild.id)

		setattr(guild, "lang", language)
		await guild.save()
		
		embed = disnake.Embed(
			description= "lang changed",
		)
		await inter.response.send_message(embed=embed)
		
def setup(bot):
	bot.add_cog(Config_Set(bot))