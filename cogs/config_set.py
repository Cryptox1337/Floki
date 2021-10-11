
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

	@set.sub_command(name = 'response_channel', description="configure a response channel")
	async def set_respone_channel(
		self,
		inter: disnake.ApplicationCommandInteraction,
		response_type = commands.param(
			desc="Select an response type that you want to configure",
			choices = [
				disnake.OptionChoice('welcome message', 'welcome'),
				disnake.OptionChoice('warning message', 'warning'),
				disnake.OptionChoice('mute message', 'mute'),
				disnake.OptionChoice('ban message', 'ban'),
				disnake.OptionChoice('kick message', 'kick')
			]
		),
		channel: disnake.TextChannel = Param(desc="Select a Text-Channel"),
	):
		result, created = await Response_Channels.get_or_create(guild_id=inter.guild.id, response_type=response_type)
		if result:
			result.channel_id = channel.id
			result.status = "enabled"
			await result.save()

		if created:
			embed = disnake.Embed(
				description= "created",
			)
		else:
			embed = disnake.Embed(
				description= "updated",
			)

		await inter.response.send_message(embed=embed)			


def setup(bot):
	bot.add_cog(Config_Set(bot))