
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import asyncio

class Mute(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.mute_loop.start()

	@tasks.loop(minutes=0.1)
	async def mute_loop(self):
		for guild in self.bot.guilds:
			server = await Guilds.get(guild_id=guild.id)
			role = disnake.utils.get(guild.roles, id=server.mute_role)
			mute_response = await getResponseChannel(guild, "mute")
			mute_list = await Mutes.filter(guild_id=guild.id, status="muted")
			
			if not role:
				perms = disnake.Permissions(send_messages=False, speak=False)
				role = await guild.create_role(name="muted", permissions=perms)
				server.mute_role = role.id
				await server.save()

			for muted in mute_list:
				user = guild.get_member(muted.user_id)
				if user:
					if await getDuration(muted.end_date) > 0 :
						if not role in user.roles:
							await user.add_roles(role, reason=muted.reason)
					else:
						if role in user.roles:
							await user.remove_roles(role, reason="mute time end")

						muted.status = "unmute"
						await muted.save()

						if mute_response:
							embed = disnake.Embed(
								color=GREEN,
								title=await get_lang(guild, 'UNMUTED'),
								)
							if user.avatar:
								embed.set_author(name=f"{user.name}", icon_url=user.avatar)
							else:
								embed.set_author(name=f"{user.name}")
							embed.add_field(name=await get_lang(guild, 'GENERAL_USER'), value="{0}".format(user))
							embed.add_field(name=await get_lang(guild, 'GENERAL_MODERATOR'), value="{0}".format(self.bot.user))
							embed.add_field(name=await get_lang(guild, 'GENERAL_REASON'), value="{0}".format("mute time end"), inline=False)
							embed.add_field(name=await get_lang(guild, 'GENERAL_COUNT'), value="{0}".format(len(await Mutes.filter(guild_id=guild.id, user_id=user.id))), inline=False)
							await mute_response.send(embed=embed)
				else:
					if await getDuration(muted.end_date) < 0 :
						muted.status = "unmute"
						await muted.save()

		
	@commands.slash_command(name = "mute", description="mute a user")
	async def mute(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User,
		reason: str = Param("no reason", desc="reason for the mute"),
		hours: int = Param(0, desc="enter a number of hours"),
		minutes: int = Param(0, desc="enter a number of minutes"),
		seconds: int = Param(0, desc="enter a number of seconds"),
	):
		duration = (hours * 60 * 60) + (minutes * 60) + seconds

		if not duration:
			duration = 525600 * 60 * 10

		status = await mute(inter.guild, inter.author, user, duration, reason)

		if status == "muted":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'MUTE_SUCCESSFULLY')).format(user.name)
			)
		elif status == "already_muted":
			embed = disnake.Embed(
				colour=RED,
				description=(await get_lang(inter.guild, 'MUTE_ALREADY_MUTED')).format(user.name)
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

	@commands.slash_command(name = "unmute", description="unmute a user")
	async def unmute(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User,
		reason: str = Param("no reason", desc="reason for the unmute"),
	):

		status = await unmute(inter.guild, inter.author, user, reason)

		if status == "unmuted":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'UNMUTE_SUCCESSFULLY')).format(user.name)
			)
		elif status == "not_muted":
			embed = disnake.Embed(
				colour=RED,
				description=(await get_lang(inter.guild, 'UNMUTE_NOT_MUTED')).format(user.name)
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)		

		await inter.response.send_message(embed=embed)


async def mute(guild, author, user, duration, reason):
	server = await Guilds.get(guild_id=guild.id)
	role = disnake.utils.get(guild.roles, id=server.mute_role)
	mute_response = await getResponseChannel(guild, "mute")

	exist = guild.get_member(user.id)

	if not exist:
		return "user_not_exist"

	if not role:
		perms = disnake.Permissions(send_messages=False, speak=False)
		role = await guild.create_role(name="muted", permissions=perms)
		server.mute_role = role.id
		await server.save()

	try:
		already_muted = await Mutes.get(guild_id=guild.id, user_id=user.id, status="muted")
	except:
		already_muted = False	
	
	if already_muted or role in user.roles:
		return "already_muted"

	await Mutes.create(
		guild_id = guild.id,
		user_id = user.id,
		author = author.id,
		reason = reason,			
		date = await getNowUTCDate(),
		end_date= await getEndUTCDate(duration),
		status = "muted",
		)

	await user.add_roles(role, reason=reason)

	if mute_response:
		embed = disnake.Embed(
			description=(await get_lang(guild, 'MUTED')).format(user.name),
			)
		if user.avatar:
			embed.set_author(name=f"{user.name}", icon_url=user.avatar)
		else:
			embed.set_author(name=f"{user.name}")
		embed.add_field(name=await get_lang(guild, 'GENERAL_USER'), value="{0}".format(user))
		embed.add_field(name=await get_lang(guild, 'GENERAL_MODERATOR'), value="{0}".format(author))
		embed.add_field(name=await get_lang(guild, 'GENERAL_REASON'), value="{0}".format(reason), inline=False)
		embed.add_field(name=await get_lang(guild, 'GENERAL_DURATION'), value=f"{await convertTimeZone(guild, await getEndUTCDate(duration))}")
		embed.add_field(name=await get_lang(guild, 'GENERAL_COUNT'), value="{0}".format(len(await Mutes.filter(guild_id=guild.id, user_id=user.id))), inline=False)
		await mute_response.send(embed=embed)

	return "muted"

async def unmute(guild, author, user, reason):
	server = await Guilds.get(guild_id=guild.id)
	role = disnake.utils.get(guild.roles, id=server.mute_role)
	mute_response = await getResponseChannel(guild, "mute")

	exist = guild.get_member(user.id)

	if not role:
		perms = disnake.Permissions(send_messages=False, speak=False)
		role = await guild.create_role(name="muted", permissions=perms)
		server.mute_role = role.id
		await server.save()

	try:
		muted = await Mutes.get(guild_id=guild.id, user_id=user.id, status="muted")
	except:
		muted = False	
	
	if exist:
		if not muted or not role in user.roles:
			return "not_muted"
	else:
		if not muted:
			return "not_muted"		

	if exist:
		await user.remove_roles(role, reason=reason)

	muted.status = "unmuted"
	muted.end_date = await getNowUTCDate()
	await muted.save()

	if mute_response:
		embed = disnake.Embed(
			description=(await get_lang(guild, 'UNMUTED')).format(user.name),
			)
		if user.avatar:
			embed.set_author(name=f"{user.name}", icon_url=user.avatar)
		else:
			embed.set_author(name=f"{user.name}")
		embed.add_field(name=await get_lang(guild, 'GENERAL_USER'), value="{0}".format(user))
		embed.add_field(name=await get_lang(guild, 'GENERAL_MODERATOR'), value="{0}".format(author))
		embed.add_field(name=await get_lang(guild, 'GENERAL_REASON'), value="{0}".format(reason), inline=False)
		embed.add_field(name=await get_lang(guild, 'GENERAL_COUNT'), value="{0}".format(len(await Mutes.filter(guild_id=guild.id, user_id=user.id))), inline=False)
		await mute_response.send(embed=embed)

	return "unmuted"


def setup(bot):
	bot.add_cog(Mute(bot))