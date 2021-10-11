
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

class Warn(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command(name = "warn", description="warn a user")
	async def warn(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User,
		reason: str = Param("no reason", desc="reason for the warn"),
	):

		status = await warn(inter.guild, inter.author, user, reason)

		if status == "USER_WARNED":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'USER_WARNED')).format(user.name)
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

async def warn(guild, author, user, reason):
	exist = guild.get_member(user.id)
	warn_response = await getResponseChannel(guild, "warn")
	user_db = await Users.get(guild_id=guild.id, user_id=user.id)

	if not exist:
		return "USER_NOT_EXIST"

	user_db.warns += 1
	await user_db.save()		

	await Warns.create(
		guild_id = guild.id,
		user_id = user.id,
		author = author.id,
		reason = reason,
		date = await getNowUTCDate(),
		)

	if warn_response:
		embed = disnake.Embed(
			color=GREEN,
			description=(await get_lang(guild, 'WARN_TITLE')).format(user.name),
			)
		if user.avatar:
			embed.set_author(name=f"{user.name}", icon_url=user.avatar)
		else:
			embed.set_author(name=f"{user.name}")
		embed.add_field(name=await get_lang(guild, 'GENERAL_USER'), value="{0}".format(user))
		embed.add_field(name=await get_lang(guild, 'GENERAL_MODERATOR'), value="{0}".format(author))
		embed.add_field(name=await get_lang(guild, 'GENERAL_REASON'), value="{0}".format(reason), inline=False)
		embed.add_field(name=await get_lang(guild, 'GENERAL_COUNT'), value="{0}".format(user_db.warns), inline=False)
		await warn_response.send(embed=embed)

	return "USER_WARNED"

def setup(bot):
	bot.add_cog(Warn(bot))