import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import asyncio

class Count_Channel(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.count_channel_loop.start()

	@tasks.loop(minutes=0.1)
	async def count_channel_loop(self):
		for guild in self.bot.guilds:
			await check_count_channel(guild)


	@commands.slash_command()
	async def count_channel(self, inter):
		pass

	@count_channel.sub_command(name = "create", description="create a count channel")
	async def create(
		self,
		inter: disnake.ApplicationCommandInteraction,
		count_name: str = Param(desc="enter name of the count channel")
	):
		await inter.response.defer()

		status, count_type = await select_count_type(inter, False)

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

		elif status == "SELECTED" and count_type:
			status = await create_count_channel(inter.guild, count_name, count_type)

			if status == "COUNT_CREATED":
				embed = disnake.Embed(
					color=GREEN,
					description=await get_lang(inter.guild, 'COUNT_CREATED')
				)
			elif status == "COUNT_ALREADY_EXIST":
				embed = disnake.Embed(
					colour=RED,
					description=await get_lang(inter.guild, 'COUNT_ALREADY_EXIST')
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

	@count_channel.sub_command(name = "remove", description="remove a count channel")
	async def remove(
		self,
		inter: disnake.ApplicationCommandInteraction
	):
		await inter.response.defer()

		status, count_type = await select_count_type(inter, True)

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

		elif status == "SELECTED" and count_type:
			status = await remove_count_channel(inter.guild, count_type)

			if status == "COUNT_REMOVED":
				embed = disnake.Embed(
					color=GREEN,
					description=await get_lang(inter.guild, 'COUNT_REMOVED')
				)
			elif status == "COUNT_NOT_EXIST":
				embed = disnake.Embed(
					colour=RED,
					description=await get_lang(inter.guild, 'COUNT_NOT_EXIST')
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


	@count_channel.sub_command(name = "update", description="update a count channel")
	async def update(
		self,
		inter: disnake.ApplicationCommandInteraction,
		count_type = commands.param(
			desc="Select an count type that you want to create",
			choices = [
				disnake.OptionChoice('User Count', 'user'),
				disnake.OptionChoice('Bot Count', 'bot'),
				disnake.OptionChoice('Channel Count', 'channel'),
			]
		),
		new_name: str = Param(None, desc="enter the new name for the count channel"),
		status = commands.param(None, desc="activate or deactivate the count channel",
			choices = [
				disnake.OptionChoice('Enable', 'enabled'),
				disnake.OptionChoice('Disable', 'disabled'),
			]
		),
	):
		await inter.response.defer()

		status = await update_count_channel(inter.guild, new_name, count_type, status)

		if status == "COUNT_UPATED":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'COUNT_UPATED')
			)
		elif status == "NOTHING_TO_CHANGE":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'NOTHING_TO_CHANGE')
			)

		elif status == "COUNT_NOT_EXIST":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'COUNT_NOT_EXIST')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)

		await inter.edit_original_message(embed=embed)


async def select_count_type(inter, exist):
	count_channels = await Count_Channels.filter(guild_id=inter.guild.id)
	option_list = []
	if exist:
		if count_channels:
			for count_channel in count_channels:
				option_list.append(disnake.SelectOption(label=count_channel.count_type.capitalize(), value=count_channel.count_type))

	else:
		count_types = ["channel", "user", "bot"]

		if count_channels:
			for count_channel in count_channels:
				for count_type in count_types:
					if count_type == count_channel.count_type:
						count_types.remove(count_type)


		if count_types:
			for count_type in count_types:
				option_list.append(disnake.SelectOption(label=count_type.capitalize(), value=count_type))

	if not option_list:
		return "NOTHING_TO_SELECT", None

	view = disnake.ui.View(timeout=10)
	dropdown = disnake.ui.Select(placeholder="choose a type that you want to configure", min_values=1, max_values=1, options=[*option_list])
	view.add_item(dropdown)

	embed = disnake.Embed(
		description="choose a type that you want to configure"
	)

	msg = await inter.edit_original_message(embed=embed, view=view)

	def check(menu_inter):
		return menu_inter.author == inter.author and menu_inter.message.id == msg.id
	try:
		menu_inter = await inter.bot.wait_for('dropdown', check=check, timeout=60)
	except asyncio.TimeoutError:
		return "NOTHING_SELECTED", None

	for value in menu_inter.values:
		count_type = value

	return "SELECTED", count_type



async def create_count_channel(guild, count_name, count_type):
	already_exist = await Count_Channels.filter(guild_id=guild.id, count_type=count_type).first()

	if already_exist:
		return "COUNT_ALREADY_EXIST"

	count = 0
	if count_type == "user":
		for user in guild.members:
			if not user.bot:
				count += 1

	if count_type == "bot":
		for user in guild.members:
			if user.bot:
				count += 1

	overwrites = {
		guild.default_role: disnake.PermissionOverwrite(
			connect=False
		)
	}

	channel = await guild.create_voice_channel(name=f"{count_name}: {count}", overwrites=overwrites)

	await Count_Channels.create(
		guild_id = guild.id,
		count_name=count_name,
		count_type = count_type,
		channel_id = channel.id,
		status = "enabled"
	)

	return "COUNT_CREATED"


async def remove_count_channel(guild, count_type):
	count_table = await Count_Channels.filter(guild_id=guild.id, count_type=count_type).first()

	if not count_table:
		return "COUNT_NOT_EXIST"

	channel = guild.get_channel(count_table.channel_id)

	if channel:
		await channel.delete()

	await count_table.delete()

	return "COUNT_REMOVED"


async def update_count_channel(guild, new_name, count_type, status):
	count_table = await Count_Channels.filter(guild_id=guild.id, count_type=count_type).first()

	if not count_table:
		return "COUNT_NOT_EXIST"

	if not new_name and not status:
		return "NOTHING_TO_CHANGE"

	if new_name:
		count_table.count_name = new_name
		await count_table.save()


	if status:
		count_table.status = status
		await count_table.save()


	return "COUNT_UPATED"

async def check_count_channel(guild):
	count_channels = await Count_Channels.filter(guild_id=guild.id, status="enabled")

	for count_channel in count_channels:
		count = 0
		if count_channel.count_type == "user":
			for user in guild.members:
				if not user.bot:
					count += 1
		if count_channel.count_type == "bot":
			for user in guild.members:
				if user.bot:
					count += 1
		if count_channel.count_type == "channel":
			count = len(guild.channels)
		
		
		channel = guild.get_channel(count_channel.channel_id)
		new_name = f"{count_channel.count_name}: {count}"
		if channel:
			if not channel.name == new_name:

				position = channel.position

				await channel.delete()

				new_channel = await channel.clone(name=new_name)

				await new_channel.edit(position=position)

				count_channel.channel_id = new_channel.id
				await count_channel.save()

		else:
			new_channel = await guild.create_voice_channel(name=new_name)
			count_channel.channel_id = new_channel.id
			await count_channel.save()



def setup(bot):
	bot.add_cog(Count_Channel(bot))