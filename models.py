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
