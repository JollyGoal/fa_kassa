from tortoise import models, fields
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

class Status(BaseModel):
    message: str


class User(models.Model):
    """Модель пользователя"""
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100, null=True)
    date_join = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)

    items: fields.ReverseRelation["Item"]


class Item(models.Model):
    """Модель items"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True)
    min_per = fields.IntField()
    max_per = fields.IntField()
    price = fields.FloatField()
    quantity = fields.IntField()
    date = fields.DatetimeField()
    # image = fields.BinaryField()
    owner: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        'models.User', related_name='items'
    )

    def min_price(self) -> float:
        return self.price + ((self.price * self.min_per)/100)

    def mid_price(self) -> float:
        mid = (self.max_per + self.min_per)/2
        return self.price + ((self.price * mid)/100)

    def max_price(self) -> float:
        return self.price + ((self.price * self.max_per)/100)

    class PydanticMeta:
        computed = ("min_price", "mid_price", "max_price")


"""Пользователи"""
UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserPydanticList = pydantic_queryset_creator(User)
UserInPydanticList = pydantic_queryset_creator(User, include=('id',))


"""Продукт"""
ItemPydantic = pydantic_model_creator(Item, name="Items")
ItemInPydantic = pydantic_model_creator(Item, name="ItemsIn", exclude_readonly=True)
ItemPydanticList = pydantic_queryset_creator(Item)