from peewee import *

db = SqliteDatabase('database.sqlite')

class BaseModel(Model):
	class Meta:
		database = db

class User(BaseModel):
	username = CharField()
	password = CharField()
	salt = CharField()


class File(BaseModel):
	modified = DateTimeField()
	hash = CharField()

class UserHasFiles(BaseModel):
	file = ForeignKeyField(File, backref='users')
	user = ForeignKeyField(User, backref='files')

db.connect()

db.create_tables([User, File, UserHasFiles])
