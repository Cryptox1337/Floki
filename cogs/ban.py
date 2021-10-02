
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import asyncio

class Ban(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.ban_loop.start()

	@tasks.loop(minutes=0.1)
	async def ban_loop(self):
		for guild in self.bot.guilds:
			server = await Guilds.get(guild_id=guild.id)
			ban_response = await getResponseChannel(guild, "ban")
			ban_list = await Bans.filter(guild_id=guild.id, status="banned")
			
			for ban in ban_list:
				user = await self.bot.fetch_user(ban.user_id)

				if await getDuration(ban.end_date) > 0 :
					if not await getIsUserBanned(guild, ban.user_id):
						await guild.ban(user, reason=ban.reason)
				else:
					if await getIsUserBanned(guild, ban.user_id):
						await guild.unban(user, reason="ban time end")

					ban.status = "unbanned"
					await ban.save()

					if ban_response:
						embed = disnake.Embed(
							color=GREEN,
							title=await get_lang(guild, 'BAN_TITLE'),
							)
						embed.set_author(name=f"{user.name}", icon_url=user.avatar) 
						embed.add_field(name=await get_lang(guild, 'GENERAL_USER'), value="{0}".format(user))
						embed.add_field(name=await get_lang(guild, 'GENERAL_MODERATOR'), value="{0}".format(self.bot.user))
						embed.add_field(name=await get_lang(guild, 'GENERAL_REASON'), value="{0}".format("ban time end"), inline=False)
						await ban_response.send(embed=embed)


		
	@commands.slash_command(name = "ban", description="ban a user")
	async def ban(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User,
		reason: str = Param("no reason", desc="reason for the ban"),
		hours: int = Param(0, desc="enter a number of hours"),
		minutes: int = Param(0, desc="enter a number of minutes"),
		seconds: int = Param(0, desc="enter a number of seconds"),
	):
		duration = (hours * 60 * 60) + (minutes * 60) + seconds

		if not duration:
			duration = 525600 * 60 * 10

		status = await ban(inter.guild, inter.author, user, duration, reason)

		if status == "banned":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'BAN_TEXT')).format(user.name)
			)
		elif status == "already_banned":
			embed = disnake.Embed(
				colour=RED,
				description=(await get_lang(inter.guild, 'ALREADY_BANNED')).format(user.name)
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


async def ban(guild, author, user, duration, reason):
	server = await Guilds.get(guild_id=guild.id)
	ban_response = await getResponseChannel(guild, "ban")

	exist = guild.get_member(user.id)

	if not exist:
		return "user_not_exist"
	try:
		already_banned = await Bans.get(guild_id=guild.id, user_id=user.id, status="banned")
	except:
		already_banned = False
	
	if already_banned or await getIsUserBanned(guild, user):
		return "already_banned"

	await Bans.create(
		guild_id = guild.id,
		user_id = user.id,
		author = author.id,
		reason = reason,			
		date = await getNowUTCDate(),
		end_date= await getEndUTCDate(duration),
		status = "banned",
		)

	await guild.ban(user, reason=reason)

	if ban_response:
		embed = disnake.Embed(
			description=(await get_lang(guild, 'BAN_TITLE')).format(user.name),
			)
		embed.set_author(name=f"{user.name}", icon_url=user.avatar)
		embed.add_field(name=await get_lang(guild, 'GENERAL_USER'), value="{0}".format(user))
		embed.add_field(name=await get_lang(guild, 'GENERAL_MODERATOR'), value="{0}".format(author))
		embed.add_field(name=await get_lang(guild, 'GENERAL_REASON'), value="{0}".format(reason), inline=False)
		embed.add_field(name=await get_lang(guild, 'GENERAL_DURATION'), value=f"{await convertTimeZone(guild, await getEndUTCDate(duration))}")
		await ban_response.send(embed=embed)

	return "banned"


def setup(bot):
	bot.add_cog(Ban(bot))