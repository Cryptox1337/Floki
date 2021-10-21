
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import random
from easy_pil import *

class Level(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			user = await Users.filter(guild_id=message.guild.id, user_id=message.author.id).first()
			if user:
				_xp_table = await XP_Table.filter()
				xp = random.uniform(15.0, 25.0)
				user.xp += xp

				new_level = None
				for xp_table in _xp_table:
					if user.xp > xp_table.xp:
						new_level = xp_table.level
					else:
						break

				if new_level and not user.level >= new_level:
					user.level = new_level
					await message.channel.send(f"GG {message.author.mention}, you just advanced to level {new_level}")

				await user.save()

	@commands.slash_command(name = "rank", description="get the rank card")
	async def get_rank_card(
		self,
		inter: disnake.ApplicationCommandInteraction,
	):

		await inter.response.defer()

		file = await create_level_card(inter.guild, inter.author)

		if file:
			await inter.edit_original_message(file=file)
		
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)
			await inter.edit_original_message(embed=embed)

async def create_level_card(guild, user):
	user_data = await Users.filter(guild_id=guild.id, user_id=user.id).first()

	if not user_data:
		return None

	current_level_table = await XP_Table.filter(level=user_data.level).first()
	next_level_table = await XP_Table.filter(level=user_data.level + 1).first()
	server_ranks = await Users.filter(guild_id=guild.id).order_by("-xp")

	rank = 0
	for server_rank in server_ranks:
		rank += 1 
		if server_rank.user_id == user.id:
			break

	if user.avatar:
		avatar = user.avatar
	else:
		avatar = user.default_avatar
		
	poppins = Font().poppins(size=38)
	poppins_middle = Font().poppins(size=35)
	poppins_small_bold = Font().poppins(variant="bold",size=25)
	poppins_small = Font().poppins(size=25)

	"""Canvas"""
	background = Editor(Canvas((934, 282), color="#23272A"))

	"""Black Background"""
	background.rectangle((24, 36), width=886, height=210, fill="#090A0B", radius=10)

	"""Profile Image"""
	background.rectangle((38, 58), width=168, height=168, fill="#000000", radius=100)
	profile = Editor(await load_image_async(str(avatar))).resize((160, 160)).circle_image()
	background.paste(profile, (42, 63))

	member = await guild.getch_member(user.id, strict=True)

	fill = 	None
	if str(member.status) == "online":
		fill = 	"#44B37F"
	elif str(member.status) == "idle":
		fill = 	"#FAA81A"

	elif str(member.status) == "dnd":
		fill = 	"#ED4245"
	elif str(member.status) == "offline":
		fill = 	"#747F8D"

	if fill:
		"""Status Symbol"""
		background.rectangle((160, 170), width=48, height=48, fill="#000000", radius=100)
		background.rectangle((164, 174), width=40, height=40, fill=fill, radius=100)


	currentxp = user_data.xp - current_level_table.xp
	nextlevelxp = next_level_table.xp - current_level_table.xp
	percentage = int(100 / nextlevelxp * currentxp)

	if percentage <= 2:
		radius = 0
	else:
		radius = 20
	
	background.rectangle((256, 182), width=636, height=40, fill="#484B4E", radius=radius)
	if not percentage <= 0:	
		background.bar((258, 184), max_width=632, height=36, percentage=percentage, fill="#62D3F5", radius=radius)

	"""Text for Username and User Discriminator"""
	name_and_discriminator_text = [
		Text(f"{user.name}", color="white", font=poppins),
		Text(f"#{user.discriminator}", color="#787C7D", font=poppins_small)
	]
	background.multicolor_text((267, 123), texts=name_and_discriminator_text)


	"""Text for Current Xp and needed XP"""
	current_and_needed_xp_text = [
		Text(f"{int(user_data.xp)}", color="#000000", font=poppins_small_bold),
		Text("/", color="#000000", font=poppins_small_bold),
		Text(f"{int(next_level_table.xp)} XP", color="#000000", font=poppins_small_bold)
	]
	background.multicolor_text((572, 185), texts=current_and_needed_xp_text, align="center")


	"""Text for Rank and Level"""
	rank_and_level_text = [
		Text("RANK", color="white", font=poppins_middle),
		Text(f"#{rank} ", color="white", font=poppins_middle),
		Text("LEVEL", color="#62D3F5", font=poppins_middle),
		Text(f"{user_data.level}", color="#62D3F5", font=poppins_middle)
	]
	background.multicolor_text((865, 40), texts=rank_and_level_text, align="right")


	file = disnake.File(fp=background.image_bytes, filename="card.png")

	return file

def setup(bot):
	bot.add_cog(Level(bot))