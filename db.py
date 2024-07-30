from peewee import *
from playhouse.migrate import SqliteMigrator, migrate

db = SqliteDatabase('people.db')


class User(Model):
    chat_id = IntegerField(unique=True)
    lang = CharField(default='en')
    is_premium = BooleanField(default=False)
    is_active = BooleanField(default=True)
    end_premium = DateTimeField(null=True)

    class Meta:
        database = db


def migrate_db():
    migrator = SqliteMigrator(db)
    try:
        migrate(
            migrator.add_column('user', 'end_premium', DateTimeField(null=True)),
            migrator.add_column('user', 'is_premium', BooleanField(default=False)),
        )
    except OperationalError:
        pass
