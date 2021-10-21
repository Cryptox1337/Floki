
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

class Config_Set(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command()
	async def set(self, inter):
		pass

	@set.sub_command(name = 'language', description="configure the language of the bot")
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
		await inter.response.defer()

		guild = await Guilds.get(guild_id=inter.guild.id)

		setattr(guild, "lang", language)
		await guild.save()
		
		embed = disnake.Embed(
			description= "lang changed",
		)

		await inter.edit_original_message(embed=embed)

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
		await inter.response.defer()

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

		await inter.edit_original_message(embed=embed)


	@set.sub_command(name = "xp-rate", description="Configure the XP-Rate")
	async def set_xp_rate(
		self,
		inter: disnake.ApplicationCommandInteraction,
		xp_rate = commands.param(
			desc="Select an response type that you want to configure",
			choices = [
				disnake.OptionChoice('x0.25', '0.25'),
				disnake.OptionChoice('x0.5', '0.5'),
				disnake.OptionChoice('x1 (default)', '1.0'),
				disnake.OptionChoice('x1.5', '1.5'),
				disnake.OptionChoice('x2', '2.0'),
				disnake.OptionChoice('x2.5', '2.5'),
				disnake.OptionChoice('x3', '3.0')
			]
		),
	):
		await inter.response.defer()

		guild_settings = await Guilds.filter(guild_id=inter.guild.id).first()

		if guild_settings:
			guild_settings.xp_rate = float(xp_rate)
			await guild_settings.save()

			embed = disnake.Embed(
				colour=GREEN,
				description=await get_lang(inter.guild, 'RANK_XP_RATE_SET')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		await inter.edit_original_message(embed=embed)


def setup(bot):
	bot.add_cog(Config_Set(bot))