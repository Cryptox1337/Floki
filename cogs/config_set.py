
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import asyncio

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


	@set.sub_command(name = "xp-roles", description="You can set roles here that will allow or disallow users from gaining XP.")
	async def set_xp_roles(
		self,
		inter: disnake.ApplicationCommandInteraction,
		option = commands.param(
			desc="allow or disallow roles to gaining xp",
			choices = [
				disnake.OptionChoice('allow', "allow"),
				disnake.OptionChoice('disallow', "disallow")
			]
		),
	):
		await inter.response.defer()

		status, role_ids = await select_xp_roles(inter, option)

		if status == "NOTHING_TO_SELECT":
			embed = disnake.Embed(
				color=RED,
				description=await get_lang(inter.guild, 'NOTHING_TO_SELECT')
			)
		elif status == "NOTHING_SELECTED":
			embed = disnake.Embed(
				color=RED,
				description=await get_lang(inter.guild, 'NOTHING_SELECTED')
			)

		elif status == "SELECTED" and role_ids:
			if option == "allow":
				description = await get_lang(inter.guild, 'XP_ROLE_ALLOWED_SUCCESFULLY')
			else:
				description = await get_lang(inter.guild, 'XP_ROLE_DISALLOWED_SUCCESFULLY')

			embed = disnake.Embed(
				description=description,
			)

			for role_id in role_ids:
				role = await Roles.filter(guild_id=inter.guild.id, role_id=role_id).first()
				if role:
					role_obj = inter.guild.get_role(int(role_id))
					
					if option == "allow":
						role.xp_role = True
					else:
						role.xp_role = False

					await role.save()

					if role_obj:
						embed.add_field(name="Role:", value=role_obj.name, inline=False)					

		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		await inter.edit_original_message(embed=embed, view=None)

	@set.sub_command(name = "xp-channels", description="You can set channels here that will allow or disallow users from gaining XP.")
	async def set_xp_channels(
		self,
		inter: disnake.ApplicationCommandInteraction,
		option = commands.param(
			desc="allow or disallow channels to gaining xp",
			choices = [
				disnake.OptionChoice('allow', "allow"),
				disnake.OptionChoice('disallow', "disallow")
			]
		),
	):
		await inter.response.defer()

		status, channel_ids = await select_xp_channels(inter, option)

		if status == "NOTHING_TO_SELECT":
			embed = disnake.Embed(
				color=RED,
				description=await get_lang(inter.guild, 'NOTHING_TO_SELECT')
			)
		elif status == "NOTHING_SELECTED":
			embed = disnake.Embed(
				color=RED,
				description=await get_lang(inter.guild, 'NOTHING_SELECTED')
			)

		elif status == "SELECTED" and channel_ids:
			if option == "allow":
				description = await get_lang(inter.guild, 'XP_CHANNEL_ALLOWED_SUCCESFULLY')
			else:
				description = await get_lang(inter.guild, 'XP_CHANNEL_DISALLOWED_SUCCESFULLY')

			embed = disnake.Embed(
				description=description,
			)

			for channel_id in channel_ids:
				channel = await Channels.filter(guild_id=inter.guild.id, channel_id=channel_id).first()
				if channel:
					channel_obj = inter.guild.get_channel(int(channel_id))
					
					if option == "allow":
						channel.xp_channel = True
					else:
						channel.xp_channel = False

					await channel.save()

					if channel_obj:
						embed.add_field(name="Channel:", value=channel_obj.name, inline=False)					

		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		await inter.edit_original_message(embed=embed, view=None)



async def select_xp_roles(inter, option):
	if option == "allow":
		roles = await Roles.filter(guild_id=inter.guild.id, xp_role=False)
	else:
		roles = await Roles.filter(guild_id=inter.guild.id, xp_role=True)

	if not roles:
		return "NOTHING_TO_SELECT", None

	option_list = []
	for role in roles:
		role_obj = inter.guild.get_role(role.role_id)
		if role_obj:
			option_list.append(disnake.SelectOption(label=role_obj.name, value=role_obj.id))


	if not option_list:
		return "NOTHING_TO_SELECT", None

	view = disnake.ui.View(timeout=10)
	dropdown = disnake.ui.Select(placeholder=f"Choose the roles you want to {option}", min_values=1, max_values=len(option_list), options=[*option_list])
	view.add_item(dropdown)

	embed = disnake.Embed(
		description=f"Choose the roles you want to {option}"
	)

	msg = await inter.edit_original_message(embed=embed, view=view)

	def check(menu_inter):
		return menu_inter.author == inter.author and menu_inter.message.id == msg.id
	try:
		menu_inter = await inter.bot.wait_for('dropdown', check=check, timeout=60)
	except asyncio.TimeoutError:
		return "NOTHING_SELECTED", None


	return "SELECTED", menu_inter.values


async def select_xp_channels(inter, option):
	xp_channel = True
	if option == "allow":
		xp_channel = False

	option_list = []
	for channel in inter.guild.text_channels:
		channel_db = await Channels.filter(guild_id=inter.guild.id, channel_id=channel.id,xp_channel=xp_channel).first()
		if channel_db:
			option_list.append(disnake.SelectOption(label=f"# {channel.name}", value=channel.id))

	if not option_list:
		return "NOTHING_TO_SELECT", None

	view = disnake.ui.View(timeout=10)
	dropdown = disnake.ui.Select(placeholder=f"Choose the channels you want to {option}", min_values=1, max_values=len(option_list), options=[*option_list])
	view.add_item(dropdown)

	embed = disnake.Embed(
		description=f"Choose the channels you want to {option}"
	)

	msg = await inter.edit_original_message(embed=embed, view=view)

	def check(menu_inter):
		return menu_inter.author == inter.author and menu_inter.message.id == msg.id
	try:
		menu_inter = await inter.bot.wait_for('dropdown', check=check, timeout=60)
	except asyncio.TimeoutError:
		return "NOTHING_SELECTED", None


	return "SELECTED", menu_inter.values

def setup(bot):
	bot.add_cog(Config_Set(bot))