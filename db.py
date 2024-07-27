from peewee import *

db = SqliteDatabase('people.db')


class User(Model):
    chat_id = IntegerField(unique=True)
    lang = CharField(default='en')
    is_active = BooleanField(default=True)

    class Meta:
        database = db
