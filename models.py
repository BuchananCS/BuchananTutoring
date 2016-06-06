from peewee import *
from flask import Blueprint

models_app = Blueprint('Models', __name__)



DATABASE_LOC = 'database.db'
try:
    db = SqliteDatabase(DATABASE_LOC)
except:
    print("Failure to open database")

class BaseModel(Model):
    class Meta:
        database = db


class Class(BaseModel):
    id = PrimaryKeyField()
    classCode = CharField()
    bookTitle = CharField(null=True)


class User(BaseModel):
    id = PrimaryKeyField()
    firstName = CharField(max_length=50)
    lastName = CharField(max_length=50)
    zangleID = CharField(max_length=20)
    zanglePassword = CharField()
    created = DateTimeField()

class Question(BaseModel):
    id = PrimaryKeyField()
    body = CharField(max_length=300,null=True)
    image = BlobField(null=True)
    pageNumber = CharField(max_length=100,null=True)
    bookTitle = CharField(max_length=100,null=True)
    submitted = DateTimeField()
    solved = DateTimeField()
    classIndex = ForeignKeyField(Class,null=True)
    user = ForeignKeyField(User,null=True)

class Answer(BaseModel):
    id = ForeignKeyField(Question)
    body = CharField(max_length=1000, null=True)
    image = BlobField(null=True)
    aid = PrimaryKeyField()




db.connect()
db.create_tables([Answer,Class,User],safe=True)
#db.drop_tables([Answer],safe=True)

