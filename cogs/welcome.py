
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from cogs.utils import *
import easy_pil

class Welcome(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, user):
		welcome_response = await getResponseChannel(user.guild, "welcome")

		if welcome_response:
			file = await create_welcome_card(user.guild, user)
			if file:
				await welcome_response.send(file=file)
	
async def create_welcome_card(guild, user):
	
	poppins = easy_pil.Font().poppins(size=50, variant="bold")
	poppins_middle = easy_pil.Font().poppins(size=30, variant="bold")
	poppins_small =  easy_pil.Font().poppins(size=25, variant="regular")

	background = easy_pil.Editor(easy_pil.Canvas((500, 500), color="#23272A"))

	if user.avatar:
		avatar = user.avatar
	else:
		avatar = user.default_avatar

	profile_x = 168
	profile_y = 50

	profile = easy_pil.Editor(await easy_pil.load_image_async(str(avatar))).resize((165, 165)).circle_image()
	background.paste(profile, (profile_x, profile_y))

	profile_corner = easy_pil.Editor("asset/round.png").resize((175, 175)).circle_image()
	background.paste(profile_corner, (profile_x - 6, profile_y - 6))


	background.text((250, 260), "WELCOME", color="white", font=poppins, align="center")

	background.text((250, 350), f"{str(user)}", color="white", font=poppins_middle, align="center")

	member_count = len(guild.members)

	if member_count == 1:
		member_count_string = f"{member_count}st"
	elif member_count == 2:
		member_count_string = f"{member_count}nd"
	elif member_count == 3:
		member_count_string = f"{member_count}rd"
	else:
		member_count_string = f"{member_count}th"

	background.text(
		(250, 450),
		f"You are the {member_count_string} Member",
		color="#0BE7F5",
		font=poppins_small,
		align="center",
	)

	file = disnake.File(fp=background.image_bytes, filename="card.png")

	return file


def setup(bot):
	bot.add_cog(Welcome(bot))