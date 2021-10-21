
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

class Kick(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command()
	async def kick(self, inter):
		pass

	@kick.sub_command(name = "kick", description="kick a user")
	async def kick_user(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User = Param(desc="The target @user"),
		reason: str = Param("no reason", desc="reason for the kick"),
	):
		await inter.response.defer()

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

		await inter.edit_original_message(embed=embed)

	@kick.sub_command(name = "list", description="get a list of the last 8 kicks")
	async def kick_list(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User = Param(None, desc="The target @user"),
	):
		await inter.response.defer()

		status, embed = await kick_list(inter.guild, user, inter.bot)

		if status == "NOTHING_FOUND":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'NOTHING_FOUND')
			)

		elif status == "KICK_LIST" and embed:
			pass

		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		
		await inter.edit_original_message(embed=embed)

async def kick_list(guild, user, bot):
	if user:
		kicks = await Kicks.filter(guild_id=guild.id, user_id=user.id).order_by("-date")
	else:
		kicks = await Kicks.filter(guild_id=guild.id).order_by("-date")

	if not kicks:
		return "NOTHING_FOUND", None

	embed = disnake.Embed(
		title="Latest Kicks",
		)

	count = 0
	for kick in kicks:
		user = await bot.fetch_user(kick.user_id)
		
		if count >= 8:
			break

		if user:
			embed.add_field(name="User:", value=user.name)
		else:
			embed.add_field(name="User:", value=kick.user_id)

		embed.add_field(name="Date:", value=await convertTimeZone(guild, kick.date))
		embed.add_field(name="Reason:", value=kick.reason)

		count += 1

	return "KICK_LIST", embed


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