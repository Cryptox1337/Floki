import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *

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
		count_name: str = Param(desc="enter name of the count channel"),
		count_type = commands.param(
			desc="Select an count type that you want to create",
			choices = [
				disnake.OptionChoice('User Count', 'user'),
				disnake.OptionChoice('Bot Count', 'bot'),
				disnake.OptionChoice('Channel Count', 'channel'),
			]
		),
	):
		status = await create_count_channel(inter.guild, count_name, count_type)

		if status == "count_channel_created":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'COUNT_CREATED')
			)
		elif status == "count_already_exist":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'COUNT_ALREADY_EXIST')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)		

		await inter.response.send_message(embed=embed)

	@count_channel.sub_command(name = "remove", description="remove a count channel")
	async def remove(
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
	):
		status = await remove_count_channel(inter.guild, count_type)

		if status == "count_channel_removed":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'COUNT_REMOVED')
			)
		elif status == "count_not_exist":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'COUNT_NOT_EXIST')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)		

		await inter.response.send_message(embed=embed)

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
		status = await update_count_channel(inter.guild, new_name, count_type, status)

		if status == "count_channel_updated":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'COUNT_UPATED')
			)
		elif status == "nothing_to_change":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'NOTHING_TO_CHANGE')
			)

		elif status == "count_not_exist":
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'COUNT_NOT_EXIST')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)		

		await inter.response.send_message(embed=embed)


async def create_count_channel(guild, count_name, count_type):
	already_exist = await Count_Channels.filter(guild_id=guild.id, count_type=count_type).first()

	if already_exist:
		return "count_already_exist"

	count = 0
	if count_type == "user":
		for user in guild.members:
			if not user.bot:
				count += 1

	if count_type == "bot":
		for user in guild.members:
			if user.bot:
				count += 1

	channel = await guild.create_voice_channel(name=f"{count_name}: {count}")

	await Count_Channels.create(
		guild_id = guild.id,
		count_name=count_name,
		count_type = count_type,
		channel_id = channel.id,
		status = "enabled"
	)

	return "count_channel_created"


async def remove_count_channel(guild, count_type):
	count_table = await Count_Channels.filter(guild_id=guild.id, count_type=count_type).first()

	if not count_table:
		return "count_not_exist"

	channel = guild.get_channel(count_table.channel_id)

	if channel:
		await channel.delete()

	await count_table.delete()

	return "count_channel_removed"


async def update_count_channel(guild, new_name, count_type, status):
	count_table = await Count_Channels.filter(guild_id=guild.id, count_type=count_type).first()

	if not count_table:
		return "count_not_exist"

	if not new_name and not status:
		return "nothing_to_change"

	if new_name:
		count_table.count_name = new_name
		await count_table.save()


	if status:
		count_table.status = status
		await count_table.save()


	return "count_channel_updated"

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