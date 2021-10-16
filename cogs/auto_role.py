import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

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


	
def setup(bot):
	bot.add_cog(Auto_Role(bot))