from enum import auto
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import asyncio

class Auto_Role(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command()
	async def auto_role(self, inter):
		pass

	@auto_role.sub_command(name = "create", description="create a new auto role")
	async def create_auto_role(
		self,
		inter: disnake.ApplicationCommandInteraction,
		role: disnake.Role = Param(None, desc="Select a Role"),
	):
		await inter.response.defer()

		status = await create_auto_role(inter.guild, role)

		if status == "AUTO_ROLE_CREATED":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'AUTO_ROLE_CREATED')
			)
		elif status == "ALREADY_AUTO_ROLE":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'ALREADY_AUTO_ROLE')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		await inter.edit_original_message(embed=embed)

	@auto_role.sub_command(name = "remove", description="remove auto role")
	async def remove_auto_role(
		self,
		inter: disnake.ApplicationCommandInteraction
	):
		await inter.response.defer()

		status, roles = await select_auto_roles(inter)

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

		elif status == "SELECTED" and roles:
			status = await remove_auto_roles(inter.guild, roles)

			if status == "AUTO_ROLE_REMOVED":
				embed = disnake.Embed(
					color=GREEN,
					description=await get_lang(inter.guild, 'AUTO_ROLE_REMOVED')
				)
			else:
				embed = disnake.Embed(
					colour=RED,
					description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
				)

		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		await inter.edit_original_message(embed=embed, view=None)

	@commands.Cog.listener()
	async def on_member_join(self, user):
		auto_roles = await Roles.filter(guild_id=user.guild.id, auto_role=True)

		for auto_role in auto_roles:
			role = user.guild.get_role(auto_role.role_id)
			if role not in user.roles:
				await user.add_roles(role, reason="auto_role")


async def create_auto_role(guild, role):
	if not role:
		role = await guild.create_role(name="new_auto_role", reason="create auto_role")
		await Roles.get_or_create(guild_id=guild.id, role_id=role.id)

	role_table = await Roles.filter(guild_id=guild.id, role_id=role.id).first()

	if role_table:
		if not role_table.auto_role:
			role_table.auto_role = True
			await role_table.save()
		else:
			return "ALREADY_AUTO_ROLE"

	return "AUTO_ROLE_CREATED"

async def select_auto_roles(inter):
	auto_roles = await Roles.filter(guild_id=inter.guild.id, auto_role=True)
	option_list = []

	if auto_roles:
		for auto_role in auto_roles:
			role = inter.guild.get_role(auto_role.role_id)
			option_list.append(disnake.SelectOption(label=role.name, value=auto_role.id))

	if not option_list:
		return "NOTHING_TO_SELECT", None

	view = disnake.ui.View(timeout=10)
	dropdown = disnake.ui.Select(placeholder="select auto roles that you want to remove", min_values=1, max_values=len(option_list), options=[*option_list])
	view.add_item(dropdown)

	embed = disnake.Embed(
		description="select auto roles that you want to remove"
	)

	msg = await inter.edit_original_message(embed=embed, view=view)

	def check(menu_inter):
		return menu_inter.author == inter.author and menu_inter.message.id == msg.id
	try:
		menu_inter = await inter.bot.wait_for('dropdown', check=check, timeout=60)
	except asyncio.TimeoutError:
		return "NOTHING_SELECTED", None

	return "SELECTED", menu_inter.values

async def remove_auto_roles(guild, auto_roles):
	for auto_role in auto_roles:
		auto_role = await Roles.filter(id=auto_role, guild_id=guild.id, auto_role=True).first()

		if auto_role:
			auto_role.auto_role = False
			await auto_role.save()

	return	"AUTO_ROLE_REMOVED"


def setup(bot):
	bot.add_cog(Auto_Role(bot))