
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
			voice_configs = await Temporary_Voice_Config.filter(guild_id=guild.id, status="enabled")

			if voice_configs:
				for voice_config in voice_configs:
					voice_channel = guild.get_channel(voice_config.channel_id)
					voice_category = guild.get_channel(voice_config.category_id)

					if not voice_category:
						voice_category = await guild.create_category(name="temporary_voice_category", reason="create category for temporary voice")
						voice_config.category_id = voice_category.id
						await voice_config.save()

					if not voice_channel:
						voice_channel = await guild.create_voice_channel(name="create", category=voice_category, position=0, reason="create channel for temporary voice")
						voice_config.channel_id = voice_channel.id
						await voice_config.save()

					temp_channels = await Temporary_Voice_Channels.filter(guild_id=guild.id, config_id=voice_config.id)
					for temporary in temp_channels:
						temporary_channel = guild.get_channel(temporary.channel_id)

						if temporary_channel:
							if len(temporary_channel.members) == 0:
								await temporary.delete()
								try:
									await temporary_channel.delete()
								except:
									pass
							else:
								if not temporary_channel.category == voice_category:
									await temporary_channel.edit(category=voice_category)

								for user in temporary_channel.members:
									owner = False
									if user.id == temporary.owner_id:
										owner = user

									if not owner:
										owner = await self.bot.fetch_user(temporary.owner_id)
										new_owner = random.choice(temporary_channel.members)
										await temporary_channel.set_permissions(owner, overwrite=None)
										await temporary_channel.set_permissions(new_owner, connect=True, mute_members=True, manage_channels=True)

										temporary.owner_id = new_owner.id
										await temporary.save()

						else:
							await temporary.delete()	

					if not voice_channel.category == voice_category:
						await voice_channel.edit(category=voice_category, position=0)

					if not voice_channel.position == 0:
						await voice_channel.edit(position=0)							



	@commands.slash_command(name = "temporary_voice", description="create temporary_voice")
	async def temporary_voice(
		self,
		inter: disnake.ApplicationCommandInteraction,
		category: disnake.CategoryChannel = Param(None,desc="Select a Categorie"),
		limit: int = Param(0, desc="amount between 0 - 99"),
		bitrate: int = Param(64, desc="amount between 8Kbps - 96Kbps (with Boost 128Kbps)"),		
	):
		await inter.response.defer()
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

		await inter.edit_original_message(embed=embed)

	@commands.Cog.listener()
	async def on_voice_state_update(self, user, before, after):
		guild = user.guild
		voice_configs = await Temporary_Voice_Config.filter(guild_id=guild.id, status="enabled")

		if voice_configs:
			for voice_config in voice_configs:
				temp_channels = await Temporary_Voice_Channels.filter(guild_id=guild.id, config_id=voice_config.id)
				voice_channel = guild.get_channel(voice_config.channel_id)
				voice_category = guild.get_channel(voice_config.category_id)

				if not voice_category:
					voice_category = await guild.create_category(name="temporary_voice_category", reason="create category for temporary voice")
					voice_config.category_id = voice_category.id
					await voice_config.save()

				if not voice_channel:
					voice_channel = await guild.create_voice_channel(name="create", category=voice_category, position=0, reason="create channel for temporary voice")
					voice_config.channel_id = voice_channel.id
					await voice_config.save()

				if not voice_channel.category == voice_category:
					await voice_channel.edit(category=voice_category, position=0)

				if not voice_channel.position == 0:
					await voice_channel.edit(position=0)

				if after.channel:
					if after.channel.id == voice_config.channel_id:
						overwrites = {
						user: disnake.PermissionOverwrite(
							connect=True, mute_members=True, manage_channels=True
						),
					}


						temp_channel_name = f"{user.name}´s Talk"
	
						bitrate = voice_config.bitrate
	
						if bitrate < 8 or bitrate > int(guild.bitrate_limit / 1000):
							bitrate = 64
	
						temp_channel = await guild.create_voice_channel(
							name=temp_channel_name,
							category=voice_category,
							overwrites=overwrites,
							user_limit=voice_config.limit,
							bitrate=bitrate * 1000,
						)
						await user.move_to(temp_channel)
	
						await Temporary_Voice_Channels.create(
							guild_id = guild.id,
							owner_id = user.id,
							channel_id = temp_channel.id,
							config_id = voice_config.id,
							)

				if before.channel:
					if temp_channels:
						for temporary in temp_channels:
							if len(before.channel.members) == 0:
								if before.channel.id == temporary.channel_id:
									await temporary.delete()
									try:
										await before.channel.delete()
									except:
										pass

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
		category = await guild.create_category(name="temporary_voice_category", reason="create temporary voice category")

	create_voice = await guild.create_voice_channel(
		name="create",
		category=category,
		reason="create temporary voice channel"
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