from peewee import *
from Src.Database.Models.BaseModel import BaseModel


class UserModel(BaseModel):
    access_level = IntegerField()   # значения колеблются от 0 до 10
    vk_id = IntegerField(unique=True)
    association = CharField(max_length=100, unique=True)

    class Meta:
        db_table = "users"         # название таблицы
        order_by = ('created_at',)      # как сортированы внутри субд





