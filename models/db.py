
from tortoise.models import Model
from tortoise import fields

class ApiResponse(Model):
    id = fields.IntField(pk=True)
    api = fields.CharField(max_length=100)
    successful_hits = fields.IntField()
    timestamp = fields.DatetimeField()
