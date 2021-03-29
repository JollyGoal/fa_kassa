from tortoise import models, fields
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

class Status(BaseModel):
    message: str


class User(models.Model):
    """Модель пользователя"""
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=1000)
    is_active = fields.BooleanField(default=True)

    async def save(self, *args, **kwargs) -> None:
        self.hashed_password = "123456"
        await super().save(*args, **kwargs)

    class PydanticMeta:
        exclude = ['hashed_password']


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
    # owner = fields.ForeignKeyField('models.User', related_name='items')

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


"""Продукт"""
ItemPydantic = pydantic_model_creator(Item, name="Items", include=('id',))
ItemInPydantic = pydantic_model_creator(Item, name="ItemsIn", exclude_readonly=True)
ItemPydanticList = pydantic_queryset_creator(Item)