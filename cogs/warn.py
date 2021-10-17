
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

class Warn(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command()
	async def warn(self, inter):
		pass

	@warn.sub_command(name = "warn", description="warn a user")
	async def warn_user(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User,
		reason: str = Param("no reason", desc="reason for the warn"),
	):
		await inter.response.defer()

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

		await inter.edit_original_message(embed=embed)


	@warn.sub_command(name = "list", description="get a list of the last 8 warns")
	async def warn_list(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User = Param(None,desc="Enter a User")
	):
		await inter.response.defer()

		status, embed = await warn_list(inter.guild, user, inter.bot)

		if status == "NOTHING_FOUND":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'NOTHING_FOUND')
			)

		elif status == "WARN_LIST" and embed:
			pass

		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		
		await inter.edit_original_message(embed=embed)

async def warn_list(guild, user, bot):
	if user:
		warns = await Warns.filter(guild_id=guild.id, user_id=user.id).order_by("-date")
	else:
		warns = await Warns.filter(guild_id=guild.id).order_by("-date")

	if not warns:
		return "NOTHING_FOUND", None

	embed = disnake.Embed(
		title="Latest Bans",
		)

	count = 0
	for warn in warns:
		user = await bot.fetch_user(warn.user_id)
		
		if count >= 8:
			break

		if user:
			embed.add_field(name="User:", value=user.name)
		else:
			embed.add_field(name="User:", value=warn.user_id)

		embed.add_field(name="Date:", value=await convertTimeZone(guild, warn.date))
		embed.add_field(name="Reason:", value=warn.reason)

		count += 1

	return "WARN_LIST", embed

async def warn(guild, author, user, reason):
	exist = guild.get_member(user.id)
	warn_response = await getResponseChannel(guild, "warn")
	user_db = await Users.filter(guild_id=guild.id, user_id=user.id).first()

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