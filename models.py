from tortoise.models import Model
from tortoise import fields

class Guilds(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False, unique=True)
	lang = fields.CharField(null=False, max_length=255, default="english")
	timezone = fields.CharField(max_length=255, null=False, default="UTC")
	created = fields.DatetimeField(auto_now_add=True)
	updated = fields.DatetimeField(auto_now_add=True)
	mute_role = fields.BigIntField(null=False, default=0)
	xp_rate = fields.FloatField(null=False, default=1.0)

class Users(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	user_id = fields.BigIntField(null=False)
	level = fields.IntField(null=False, default=0)
	xp = fields.FloatField(null=False, default=0)
	warns = fields.IntField(null=False, default=0)

class Channels(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	channel_id = fields.BigIntField(null=False)
	xp_channel = fields.BooleanField(null=True, default=True)

class Roles(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	role_id = fields.BigIntField(null=False)
	auto_role = fields.BooleanField(null=True, default=False)
	xp_role = fields.BooleanField(null=True, default=True)

class Response_Channels(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	response_type = fields.CharField(null=False, max_length=255)
	channel_id = fields.BigIntField(null=False, default=0)
	status = fields.CharField(null=False, max_length=255, default="disabled")


class Mutes(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	user_id = fields.BigIntField(null=False)
	author = fields.BigIntField(null=False)
	reason = fields.CharField(null=False, max_length=255)
	date = fields.DatetimeField(null=False)
	end_date = fields.DatetimeField(null=False)
	status = fields.CharField(null=False, max_length=255, default="muted")

class Kicks(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	user_id = fields.BigIntField(null=False)
	author = fields.BigIntField(null=False)
	reason = fields.CharField(null=False, max_length=255)
	date = fields.DatetimeField(null=False)
	
class Warns(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	user_id = fields.BigIntField(null=False)
	author = fields.BigIntField(null=False)
	reason = fields.CharField(null=False, max_length=255)
	date = fields.DatetimeField(null=False)

class Bans(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	user_id = fields.BigIntField(null=False)
	author = fields.BigIntField(null=False)
	reason = fields.CharField(null=False, max_length=255)
	date = fields.DatetimeField(null=False)
	end_date = fields.DatetimeField(null=False)
	status = fields.CharField(null=False, max_length=255, default="banned")

class Temporary_Voice_Config(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	channel_id = fields.BigIntField(null=False)
	category_id = fields.BigIntField(null=False)
	limit = fields.BigIntField(null=False, default=0)
	bitrate = fields.BigIntField(null=False, default=64)
	status = fields.CharField(null=False, max_length=255, default="disabled")

class Temporary_Voice_Channels(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	owner_id = fields.BigIntField(null=False)
	channel_id = fields.BigIntField(null=False)
	config_id = fields.BigIntField(null=False)	

class Ticket_Config(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	channel_id = fields.BigIntField(null=False)
	category_id = fields.BigIntField(null=False)
	message_id = fields.BigIntField(null=False, default=0)
	status = fields.CharField(null=False, max_length=255, default="disabled")

class Tickets(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	user_id = fields.BigIntField(null=False)
	config_id = fields.BigIntField(null=False)	
	ticket_channel = fields.BigIntField(null=False)
	message_id = fields.BigIntField(null=False)
	status = fields.CharField(null=False, max_length=255, default="Open")

class Embeds(Model):	
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	title = fields.CharField(null=True, max_length=255)
	title_url = fields.CharField(null=True, max_length=255)
	description = fields.TextField(null=True, max_length=255)
	color = fields.BigIntField(null=True, max_length=255)
	author = fields.BigIntField(null=True, max_length=255)
	author_icon = fields.BooleanField(null=True)
	thumbnail = fields.CharField(null=True, max_length=255)
	image = fields.CharField(null=True, max_length=255)
	footer = fields.TextField(null=True, max_length=255)
	footer_icon = fields.CharField(null=True, max_length=255)
	status = fields.CharField(null=True, max_length=255, default="disabled")

class Count_Channels(Model):
	id = fields.IntField(pk=True)
	guild_id = fields.BigIntField(null=False)
	count_name = fields.CharField(null=False, max_length=255)
	count_type = fields.CharField(null=False, max_length=255)
	channel_id = fields.BigIntField(null=False)
	status = fields.CharField(null=False, max_length=255, default="disabled")

class XP_Table(Model):
	level = fields.IntField(pk=True)
	xp = fields.FloatField(null=False)
