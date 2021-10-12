
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import random

class Temporary_Voice(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.temporay_voice_loop.start()

	@tasks.loop(minutes=0.1)
	async def temporay_voice_loop(self):
		for guild in self.bot.guilds:
			voice_config = await Temporary_Voice_Config.filter(guild_id=guild.id, status="enabled")

			if voice_config:
				temp_channels = await Temporary_Voice_Channels.filter(guild_id=guild.id)
				for temporary in temp_channels:
					for channel in guild.voice_channels:
						if channel.id == temporary.channel_id:
							if len(channel.members) == 0:
								await channel.delete()
								await temporary.delete()
								
							else:
								for user in channel.members:
									owner = False
									if user.id == temporary.owner_id:
										owner = user

									if not owner:
										owner = await self.bot.fetch_user(temporary.owner_id)
										new_owner = random.choice(channel.members)
										await channel.set_permissions(owner, overwrite=None)
										await channel.set_permissions(new_owner, connect=True, mute_members=True, manage_channels=True)

										temporary.owner_id = new_owner.id
										await temporary.save()


	@commands.slash_command(name = "temporary_voice", description="create temporary_voice")
	async def temporary_voice(
		self,
		inter: disnake.ApplicationCommandInteraction,
		category: disnake.CategoryChannel = Param(None,desc="Select a Categorie"),
		limit: int = Param(0, desc="amount between 0 - 99"),
		bitrate: int = Param(64, desc="amount between 8Kbps - 96Kbps (with Boost 128Kbps)"),		
	):

		status = await create_temporary_voice(inter.guild, category, limit, bitrate)

		if status == "TEMPORARY_CREATED":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'TEMPORARY_CREATED')
			)
		elif status == "TEMPORARY_INCORRECT_LIMIT":
			embed = disnake.Embed(
				colour=RED,
				description=(await get_lang(inter.guild, 'TEMPORARY_INCORRECT_LIMIT')).format(limit)
			)
		elif status == "TEMPORARY_INCORRECT_BITRATE":
			embed = disnake.Embed(
				colour=RED,
				description=(await get_lang(inter.guild, 'TEMPORARY_INCORRECT_BITRATE')).format(bitrate, int(inter.guild.bitrate_limit / 1000))
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)		

		await inter.response.send_message(embed=embed)

	@commands.Cog.listener()
	async def on_voice_state_update(self, user, before, after):
		guild = user.guild
		voice_config = await Temporary_Voice_Config.filter(guild_id=guild.id, status="enabled")

		if voice_config:
			if after.channel:
				for temporary in voice_config:
					if after.channel.id == temporary.channel_id:
						overwrites = {
							user: disnake.PermissionOverwrite(
								connect=True, mute_members=True, manage_channels=True
							),
						}

						try:
							category = guild.get_channel(temporary.category_id)
						except:
							category = after.channel.category

						temp_channel_name = f"{user.name}´s Talk"

						bitrate = temporary.bitrate

						if bitrate < 8 or bitrate > int(guild.bitrate_limit / 1000):
							bitrate = 64

						temp_channel = await guild.create_voice_channel(
							name=temp_channel_name,
							category=category,
							overwrites=overwrites,
							user_limit=temporary.limit,
							bitrate=bitrate * 1000,
						)
						await user.move_to(temp_channel)

						await Temporary_Voice_Channels.create(
							guild_id = guild.id,
							owner_id = user.id,
							channel_id = temp_channel.id,
							config_id = temporary.id,
							)

			if before.channel:
				temp_channels = await Temporary_Voice_Channels.filter(guild_id=guild.id)
				if temp_channels:
					for temporary in temp_channels:
						if len(before.channel.members) == 0:
							if before.channel.id == temporary.channel_id:
								await before.channel.delete()
								await temporary.delete()

						if user.id == temporary.owner_id and not len(before.channel.members) == 0:
							new_owner = random.choice(before.channel.members)

							await before.channel.set_permissions(user, overwrite=None)
							await before.channel.set_permissions(new_owner, connect=True, mute_members=True, manage_channels=True)

							temporary.owner_id = new_owner.id
							await temporary.save()




async def create_temporary_voice(guild, category, limit, bitrate):
	if limit < 0 or limit > 99:
		return "TEMPORARY_INCORRECT_LIMIT"

	if bitrate < 8 or bitrate > int(guild.bitrate_limit / 1000):
		return "TEMPORARY_INCORRECT_BITRATE"

	if not category:
		category = await guild.create_category(name="temporary_voice_category")

	create_voice = await guild.create_voice_channel(
		name="create",
		category=category
	)

	await Temporary_Voice_Config.create(
		guild_id=guild.id,
		channel_id=create_voice.id,
		category_id=category.id,
		limit=limit,
		bitrate=bitrate,
		status="enabled"
	)

	return "TEMPORARY_CREATED"

def setup(bot):
	bot.add_cog(Temporary_Voice(bot))