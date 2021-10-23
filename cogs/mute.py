
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

class Mute(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.mute_loop.start()

	@tasks.loop(minutes=0.1)
	async def mute_loop(self):
		for guild in self.bot.guilds:
			server = await Guilds.get(guild_id=guild.id)
			role = guild.get_role(server.mute_role)
			mute_response = await getResponseChannel(guild, "mute")
			mute_list = await Mutes.filter(guild_id=guild.id, status="muted")
			
			if not role:
				perms = disnake.Permissions(send_messages=False, speak=False)
				role = await guild.create_role(name="muted", permissions=perms, reason="mute_role does not exist")
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


	@commands.slash_command(name = "mute", description="Mutes a user from the server")
	async def mute_user(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User = Param(desc="The target @user"),
		reason: str = Param("no reason", desc="Reason of the Mute"),
		hours: int = Param(0, desc="enter a number of hours"),
		minutes: int = Param(0, desc="enter a number of minutes"),
		seconds: int = Param(0, desc="enter a number of seconds"),
	):
		await inter.response.defer()

		duration = (hours * 60 * 60) + (minutes * 60) + seconds

		if not duration:
			duration = 525600 * 60 * 10

		status = await mute(inter.guild, inter.author, user, duration, reason)

		if status == "MUTE_SUCCESSFULLY":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'MUTE_SUCCESSFULLY')).format(user.name)
			)
		elif status == "MUTE_ALREADY_MUTED":
			embed = disnake.Embed(
				colour=RED,
				description=(await get_lang(inter.guild, 'MUTE_ALREADY_MUTED')).format(user.name)
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

	@commands.slash_command(name = "unmute", description="Unmutes a user")
	async def unmute(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User = Param(desc="The target @user"),
		reason: str = Param("no reason", desc="Reason of the Unmute"),
	):
		await inter.response.defer()

		status = await unmute(inter.guild, inter.author, user, reason)

		if status == "UNMUTE_SUCCESSFULLY":
			embed = disnake.Embed(
				color=GREEN,
				description=(await get_lang(inter.guild, 'UNMUTE_SUCCESSFULLY')).format(user.name)
			)
		elif status == "UNMUTE_NOT_MUTED":
			embed = disnake.Embed(
				colour=RED,
				description=(await get_lang(inter.guild, 'UNMUTE_NOT_MUTED')).format(user.name)
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		await inter.edit_original_message(embed=embed)


	@commands.slash_command(name = "mute-list", description="get a list of the last 8 mutes")
	async def mute_list(
		self,
		inter: disnake.ApplicationCommandInteraction,
		user: disnake.User = Param(None, desc="The target @user"),
	):
		await inter.response.defer()

		status, embed = await mute_list(inter.guild, user, inter.bot)

		if status == "NOTHING_FOUND":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'NOTHING_FOUND')
			)

		elif status == "MUTE_LIST" and embed:
			pass

		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		
		await inter.edit_original_message(embed=embed)

async def mute_list(guild, user, bot):
	if user:
		mutes = await Mutes.filter(guild_id=guild.id, user_id=user.id).order_by("-date")
	else:
		mutes = await Mutes.filter(guild_id=guild.id).order_by("-date")

	if not mutes:
		return "NOTHING_FOUND", None

	embed = disnake.Embed(
		title="Latest Mutes",
		)

	count = 0
	for mute in mutes:
		user = await bot.fetch_user(mute.user_id)
		
		if count >= 8:
			break

		if user:
			embed.add_field(name="User:", value=user.name)
		else:
			embed.add_field(name="User:", value=mute.user_id)

		embed.add_field(name="Date:", value=await convertTimeZone(guild, mute.date))
		embed.add_field(name="Reason:", value=mute.reason)

		count += 1

	return "MUTE_LIST", embed



async def mute(guild, author, user, duration, reason):
	server = await Guilds.get(guild_id=guild.id)
	role = guild.get_role(server.mute_role)
	mute_response = await getResponseChannel(guild, "mute")

	exist = guild.get_member(user.id)

	if not exist:
		return "USER_NOT_EXIST"

	if not role:
		perms = disnake.Permissions(send_messages=False, speak=False)
		role = await guild.create_role(name="muted", permissions=perms, reason="mute_role does not exist")
		server.mute_role = role.id
		await server.save()

	already_muted = await Mutes.filter(guild_id=guild.id, user_id=user.id, status="muted").first()
	
	if already_muted or role in user.roles:
		return "MUTE_ALREADY_MUTED"

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

	return "MUTE_SUCCESSFULLY"

async def unmute(guild, author, user, reason):
	server = await Guilds.get(guild_id=guild.id)
	role = guild.get_role(server.mute_role)
	mute_response = await getResponseChannel(guild, "mute")

	exist = guild.get_member(user.id)

	if not role:
		perms = disnake.Permissions(send_messages=False, speak=False)
		role = await guild.create_role(name="muted", permissions=perms, reason="mute_role does not exist")
		server.mute_role = role.id
		await server.save()

	muted = await Mutes.filter(guild_id=guild.id, user_id=user.id, status="muted").first()

	
	if exist:
		if not muted or not role in user.roles:
			return "UNMUTE_NOT_MUTED"
	else:
		if not muted:
			return "UNMUTE_NOT_MUTED"		

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

	return "UNMUTE_SUCCESSFULLY"


def setup(bot):
	bot.add_cog(Mute(bot))