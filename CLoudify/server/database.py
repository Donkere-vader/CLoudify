from peewee import SqliteDatabase, Model, CharField, DateTimeField, ForeignKeyField

db = SqliteDatabase('database.db')


class BaseModel(Model):
    """ Base model for all the model/ table classes """
    class Meta:
        database = db


class User(BaseModel):
    """ User table """
    username = CharField(unique=True)
    password = CharField()
    salt = CharField()
    authkey = CharField()


class File(BaseModel):
    """ File table """
    name = CharField()  # path/name.extension
    modified = DateTimeField()
    hash = CharField()
    user = ForeignKeyField(User, backref='files')


class UserHasFiles(BaseModel):
    """ UserHasFiles table | Used to keep track of what version each user has """
    file = ForeignKeyField(File, backref='users')
    user = ForeignKeyField(User, backref='device_files')


class Tables:
    User = User
    File = File
    UserHasFiles = UserHasFiles

db.connect()

db.create_tables([User, File, UserHasFiles])
