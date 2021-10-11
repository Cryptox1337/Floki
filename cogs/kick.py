
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

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

		if status == "USER_KICKED":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'USER_KICKED')).format(user.name)
			)
		elif status == "USER_NOT_EXIST":
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
		return "USER_NOT_EXIST"

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
			description=(await get_lang(guild, 'USER_KICKED')).format(user.name),
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

	return "USER_KICKED"

def setup(bot):
	bot.add_cog(Kick(bot))