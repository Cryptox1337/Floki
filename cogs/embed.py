import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import re

class Embed(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

async def create_embed(guild, title, title_url, description, color, author, author_icon, thumbnail, image, footer, footer_icon):
	if not title and description:
		return "title_or_description_required"

	if title_url:
		url_regex = re.compile(r'(http|https)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?')
		correct_url = re.findall(url_regex, title_url)

		if not correct_url:
			return "not_correct_url"


	img_list = []
	
	if thumbnail:
		img_list.append(thumbnail)

	if image:
		img_list.append(image)

	if footer_icon:
		img_list.append(footer_icon)

	for img in img_list:
		if img:
			image_regex = re.compile(r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png|jpeg|webp)')
			correct_image = re.findall(image_regex, img)

			if not correct_image:
				return "not_correct_image"


	if color > 16777215:
		return "not_correct_color"



	await Embeds.create(
		guild_id=guild.id,
		title=title,
		title_url=title_url,
		description=description,
		color=color,
		author=author,
		author_icon=author_icon,
		thumbnail=thumbnail,
		image=image,
		footer=footer,
		footer_icon=footer_icon,
		status="enabled",
	)

	return "embed_created"

async def get_embed(self, table):

	if table.color:
		color = table.color
	else:
		color = disnake.Embed.Empty

	if table.title:
		title = table.title
	else:
		title = disnake.Embed.Empty

	if table.title_url:
		url = table.title_url
	else:
		url = disnake.Embed.Empty

	if table.description:
		description = table.description
	else:
		description = disnake.Embed.Empty	

	if table.author:
		author = await self.bot.fetch_user(table.author)
	else:
		author = None

	if author:
		if author.avatar and table.author_icon:
			author_icon = author.avatar
		else:
			author_icon = disnake.Embed.Empty

	if table.footer:
		footer = table.footer
	else:
		footer = disnake.Embed.Empty

	if table.footer_icon:
		footer_icon = table.footer_icon
	else:
		footer_icon = disnake.Embed.Empty



	embed = disnake.Embed(
		colour=color,
		title=title,
		description=description,
		url=url
	)

	if table.thumbnail:
		embed.set_thumbnail(url=table.thumbnail)	
	
	if table.image:
		embed.set_image(url=table.image)

	if author:
		embed.set_author(name=author, icon_url=author_icon)

	if footer or footer_icon:
		embed.set_footer(text=footer, icon_url=footer_icon)


	return embed




def setup(bot):
	bot.add_cog(Embed(bot))