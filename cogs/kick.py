
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import asyncio

class Kick(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command(name = "kick", description="kick a user")
	async def kick(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User,
		reason: str = Param("no reason", desc="reason for the kick"),
	):

		status = await kick(inter.guild, inter.author, user, reason)

		if status == "user_kicked":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'KICK_TEXT')).format(user.name)
			)
		elif status == "user_not_exist":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'USER_NOT_EXIST')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)		

		await inter.response.send_message(embed=embed)

async def kick(guild, author, user, reason):
	exist = guild.get_member(user.id)
	kick_response = await getResponseChannel(guild, "kick")

	if not exist:
		return "user_not_exist"

	await guild.kick(user=user, reason=reason)

	await Kicks.create(
		guild_id = guild.id,
		user_id = user.id,
		author = author.id,
		reason = reason,			
		date = await getNowUTCDate(),
		)

	if kick_response:
		embed = disnake.Embed(
			color=GREEN,
			description=(await get_lang(guild, 'KICK_TEXT')).format(user.name),
			)
		if user.avatar:
			embed.set_author(name=f"{user.name}", icon_url=user.avatar)
		else:
			embed.set_author(name=f"{user.name}")
		embed.add_field(name=await get_lang(guild, 'GENERAL_USER'), value="{0}".format(user))
		embed.add_field(name=await get_lang(guild, 'GENERAL_MODERATOR'), value="{0}".format(author))
		embed.add_field(name=await get_lang(guild, 'GENERAL_REASON'), value="{0}".format(reason), inline=False)
		embed.add_field(name=await get_lang(guild, 'GENERAL_COUNT'), value="{0}".format(len(await Kicks.filter(guild_id=guild.id, user_id=user.id))), inline=False)
		await kick_response.send(embed=embed)

	return "user_kicked"

def setup(bot):
	bot.add_cog(Kick(bot))