
import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from models import *
from colors import *
from cogs.utils import *
import asyncio

class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.slash_command(name = "ticket", description="configure the ticket system")
	async def ticket(
		self,
		inter: disnake.ApplicationCommandInteraction,
		channel: disnake.TextChannel = Param(None, desc="Select a Text-Channel"),
		category: disnake.CategoryChannel = Param(None, desc="Select a Categorie"),
	):

		status = await setup_ticket_config(inter.guild, channel, category)

		if status == "TICKET_SUCCESSFULLY":
			embed = disnake.Embed(
				color=GREEN,
				description=await get_lang(inter.guild, 'TICKET_SUCCESSFULLY')
			)
		else:
			embed = disnake.Embed(
				colour=RED,
				description=await get_lang(inter.guild, 'UNKNOWN_ERROR')
			)		

		await inter.response.send_message(embed=embed)

	@commands.Cog.listener()
	async def on_interaction(self, inter: disnake.MessageInteraction):
		try:
			compnent = inter.component
		except:
			compnent = None

		if compnent:
			if compnent.custom_id == "ticket_create":
				await on_butoon_create_ticket(inter)
			elif compnent.custom_id == "ticket_lock":
				await on_butoon_ticket(inter, "ticket_lock")
			elif compnent.custom_id == "ticket_yes":
				await on_butoon_ticket(inter, "ticket_yes")
			elif compnent.custom_id == "ticket_no":
				await on_butoon_ticket(inter, "ticket_no")
			elif compnent.custom_id == "ticket_reopen":
				await on_butoon_ticket(inter, "ticket_reopen")
			elif compnent.custom_id == "ticket_close":
				await on_butoon_ticket(inter, "ticket_close")

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		configs = await Ticket_Config.filter(guild_id=channel.guild.id, status="enabled")

		if configs:
			for config in configs:
				ticket = await Tickets.filter(guild_id=channel.guild.id, config_id=config.id, ticket_channel=channel.id).first()
				if config.channel_id == channel.id or config.category_id == channel.id:
					tickets = await Tickets.filter(guild_id=channel.guild.id, config_id=config.id)
					ticket_channel = channel.guild.get_channel(config.channel_id)
					ticket_category = channel.guild.get_channel(config.category_id)

					if not ticket_category:
						ticket_category = await channel.guild.create_category(name="ticket_category")
						config.category_id = ticket_category.id

					if not ticket_channel:
						ticket_channel = await channel.guild.create_text_channel(name="ticket_channel", category=ticket_category, position=0)
						config.channel_id = ticket_channel.id

						embed, view = await get_ticket_message(channel.guild, "Create")

						msg = await ticket_channel.send(embed=embed, view=view)
						config.message_id = msg.id
						config.channel_id = ticket_channel.id
					
					if not ticket_channel.category == ticket_category:
						await ticket_channel.edit(category=ticket_category, position=0)

					if tickets:
						for ticket in tickets:
							user_ticket_channel = channel.guild.get_channel(ticket.ticket_channel)
							
							if user_ticket_channel:
								if not user_ticket_channel.category == ticket_category:
									await user_ticket_channel.edit(category=ticket_category)

							else:
								ticket.status = "Closed"
								await ticket.save()

					if not ticket_channel.position == 0:
						await ticket_channel.edit(position=0)

					await config.save()

				elif ticket:
					ticket.status = "Closed"
					await ticket.save()



	@commands.Cog.listener()
	async def on_message_delete(self, message):
		configs = await Ticket_Config.filter(guild_id=message.guild.id, status="enabled")

		if configs:
			for config in configs:
				ticket = await Tickets.filter(guild_id=message.guild.id, config_id=config.id, message_id=message.id).first()

				if config.message_id == message.id:
					ticket_channel = message.guild.get_channel(config.channel_id)
					ticket_category = message.guild.get_channel(config.category_id)

					if not ticket_category:
						ticket_category = await message.guild.create_category(name="ticket_category")
						config.category_id = ticket_category.id

					if not ticket_channel:
						ticket_channel = await message.guild.create_text_channel(name="ticket_channel", category=ticket_category)
						config.channel_id = ticket_channel.id

					embed = disnake.Embed(description = await get_lang(message.guild, 'TICKET_CREATE_EMBED'))
					view = disnake.ui.View()

					buttons = [
						disnake.ui.Button(style=disnake.ButtonStyle.green, label='ticket', custom_id="ticket_create")
					]

					for item in buttons:
						view.add_item(item)

					msg = await ticket_channel.send(embed=embed, view=view)
					config.message_id = msg.id

					await config.save()

				if ticket:
					user_ticket_channel = message.guild.get_channel(ticket.ticket_channel)

					if user_ticket_channel:
						if ticket.status == "Open":
							embed, view = await get_ticket_message(message.guild, "Open")

						elif ticket.status == "Pending":
							embed, view = await get_ticket_message(message.guild, "Pending")

						elif ticket.status == "Locked":
							embed, view = await get_ticket_message(message.guild, "Locked")

						elif ticket.status == "Closed":
							embed, view = await get_ticket_message(message.guild, "Closed")

						msg = await user_ticket_channel.send(embed=embed, view=view)

						ticket.message_id = msg.id
					
					else:
						ticket.status = "Closed"


					await ticket.save()


	@commands.Cog.listener()
	async def on_ready(self):
		for guild in self.bot.guilds:
			configs = await Ticket_Config.filter(guild_id=guild.id, status="enabled")

			for config in configs:
				tickets = await Tickets.filter(guild_id=guild.id, config_id=config.id, status__in=['Open', 'Pending', 'Locked'])

				ticket_channel = guild.get_channel(config.channel_id)
				ticket_category = guild.get_channel(config.category_id)

				if not ticket_category:
					ticket_category = await guild.create_category(name="ticket_category")
					config.category_id = ticket_category.id

				if not ticket_channel:
					ticket_channel = await guild.create_text_channel(name="ticket_channel", category=ticket_category, position=0)
					config.channel_id = ticket_channel.id

				message = ticket_channel.get_partial_message(config.message_id)

				if not ticket_channel.category == ticket_category:
					await ticket_channel.edit(category=ticket_category, position=0)

				if not message:
					embed = disnake.Embed(description = await get_lang(guild, 'TICKET_CREATE_EMBED'))
					view = disnake.ui.View()

					buttons = [
						disnake.ui.Button(style=disnake.ButtonStyle.green, label='ticket', custom_id="ticket_create")
					]

					for item in buttons:
						view.add_item(item)

					msg = await ticket_channel.send(embed=embed, view=view)
					config.message_id = msg.id

				await config.save()

				if tickets:
					for ticket in tickets:
						user_ticket_channel = guild.get_channel(ticket.ticket_channel)

						if user_ticket_channel:
							message = user_ticket_channel.get_partial_message(ticket.message_id)
							
							if not user_ticket_channel.category == ticket_category:
								await user_ticket_channel.edit(category=ticket_category)

							if not message:
								if ticket.status == "Open":
									embed, view = await get_ticket_message(guild, "Open")

								elif ticket.status == "Pending":
									embed, view = await get_ticket_message(guild, "Pending")

								elif ticket.status == "Locked":
									embed, view = await get_ticket_message(guild,"Locked")

								elif ticket.status == "Closed":
									embed, view = await get_ticket_message(guild,"Closed")


								msg = await user_ticket_channel.send(embed=embed, view=view)

								ticket.message_id = msg.id

						else:
							ticket.status = "Closed"

					await ticket.save()

				if not ticket_channel.position == 0:
					await ticket_channel.edit(position=0)	


async def setup_ticket_config(guild, channel, category):
	if not category and not channel:
		category = await guild.create_category(name="ticket_category")
		channel = await guild.create_text_channel(name="ticket_channel", category=category)
	elif not category:
		category = await guild.create_category(name="ticket_category")
		await channel.edit(category=category)
	elif not channel:
		channel = await guild.create_text_channel(name="ticket_channel", category=category)
	else:
		return

	embed = disnake.Embed(description = await get_lang(guild, 'TICKET_CREATE_EMBED'))

	view = disnake.ui.View()
	buttons = [
		disnake.ui.Button(style=disnake.ButtonStyle.green, label='ticket', custom_id="ticket_create")
	]

	for item in buttons:
		view.add_item(item)
	
	message = await channel.send(embed=embed, view=view)

	await Ticket_Config.create(
		guild_id = guild.id,
		channel_id = channel.id,	
		category_id = category.id,
		message_id = message.id,
		status = "enabled",
		)

	return "TICKET_SUCCESSFULLY"

async def on_butoon_create_ticket(inter):
	ticket_configs = await Ticket_Config.filter(guild_id=inter.guild.id, status="enabled")
	if ticket_configs:
		for config in ticket_configs:
			if config.message_id == inter.message.id:
				await create_new_ticket(inter.guild, inter.author, config)


async def create_new_ticket(guild, user, config):
	overwrites = {
		guild.default_role: disnake.PermissionOverwrite(
			read_messages=False
		),
		guild.me: disnake.PermissionOverwrite(read_messages=True),
		user: disnake.PermissionOverwrite(read_messages=True),
	}

	category = disnake.get(guild.categories, id=config.category_id)

	if not category:
		category = await guild.create_category(name="ticket_category")
		config.category_id = category.id
		await config.save()

	channel = await guild.create_text_channel("user-ticket", overwrites=overwrites, category=category)

	view = disnake.ui.View()
	buttons = disnake.ui.Button(style=disnake.ButtonStyle.green, label= await get_lang(guild, 'GENERAL_CLOSE'), custom_id="ticket_lock")
	view.add_item(buttons)

	embed = disnake.Embed(description = await get_lang(guild, 'TICKET_OPEN_EMBED'))
	msg = await channel.send(embed=embed, view=view)

	await Tickets.create(
		guild_id = guild.id,
		user_id = user.id,
		config_id = config.id,
		ticket_channel = channel.id,
		message_id = msg.id,
		status = "Open"
	)


async def on_butoon_ticket(inter, custom_id):
	closed = False
	ticket = await Tickets.filter(guild_id=inter.guild.id, ticket_channel=inter.channel.id).first()
	
	if not ticket:
		return

	if custom_id == "ticket_lock":
		ticket.status = "Pending"
		embed, view = await get_ticket_message(inter.guild, "Pending")

	elif custom_id == "ticket_yes":
		ticket.status = "Locked"
		embed, view = await get_ticket_message(inter.guild, "Locked")

		for user in inter.channel.members:
			await inter.channel.set_permissions(user, read_messages=False)


	elif custom_id == "ticket_no" or custom_id == "ticket_reopen":
		user = inter.guild.get_member(ticket.user_id)

		ticket.status = "Open"
		embed, view = await get_ticket_message(inter.guild, "Open")

		if user:
			await inter.channel.set_permissions(user, read_messages=True)


	elif custom_id == "ticket_close":
		ticket.status = "Closed"
		embed, view = await get_ticket_message(inter.guild, "Closed")
		closed = True


	try:
		await inter.response.edit_message(embed=embed, view=view)
	except:
		await inter.edit_original_message(embed=embed, view=view)		

	await ticket.save()

	if closed:
		await asyncio.sleep(5)
		await inter.channel.delete()

async def get_ticket_message(guild, name):
	if name == "Create":
		embed = disnake.Embed(description = await get_lang(guild, 'TICKET_CREATE_EMBED'))
		view = disnake.ui.View()
		buttons = [
			disnake.ui.Button(style=disnake.ButtonStyle.green, label='ticket', custom_id="ticket_create")
		]


	elif name == "Open":
		embed = disnake.Embed(description = await get_lang(guild, 'TICKET_OPEN_EMBED'))
		view = disnake.ui.View()
		buttons = [
			disnake.ui.Button(style=disnake.ButtonStyle.green, label = await get_lang(guild, 'GENERAL_CLOSE'), custom_id="ticket_lock")
		]

	elif name == "Pending":
		embed = disnake.Embed(description = await get_lang(guild, 'TICKET_PENDING_EMBED'))
		view = disnake.ui.View()
		buttons = [
					disnake.ui.Button(style=disnake.ButtonStyle.green, label = await get_lang(guild, 'GENERAL_YES'), custom_id="ticket_yes"), 
					disnake.ui.Button(style=disnake.ButtonStyle.red, label = await get_lang(guild, 'GENERAL_NO'), custom_id="ticket_no")
				]

	elif name == "Locked":
		embed = disnake.Embed(description = await get_lang(guild, 'TICKET_LOCKED_EMBED'))
		view = disnake.ui.View()
		buttons = [
					disnake.ui.Button(style=disnake.ButtonStyle.green, label = await get_lang(guild, 'GENERAL_REOPEN'), custom_id="ticket_reopen"),
					disnake.ui.Button(style=disnake.ButtonStyle.red, label = await get_lang(guild, 'GENERAL_CLOSE'), custom_id="ticket_close")
				]

	elif name == "Closed":
		embed = disnake.Embed(description = await get_lang(guild, 'TICKET_CLOSED_EMBED'))
		view = None
		buttons = None

	else:
		return None, None


	if buttons:
		for item in buttons:
			view.add_item(item)


	return embed, view




def setup(bot):
	bot.add_cog(Ticket(bot))