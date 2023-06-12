from mongoengine import Document, CASCADE, connect
from mongoengine.fields import BooleanField, ReferenceField, StringField, ListField


# connect(host="mongodb+srv://sabotab2000:FY0bThduF3hbN6dq@sabotab2401.qnlmxn8.mongodb.net/web11_1", ssl=True)

class Author(Document):
    fullname = StringField(max_length=120, required=True, unique=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=100)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()


class User(Document):
    fullname = StringField(max_length=120, required=True)
    email = StringField(max_length=50, required=True)
    is_sent = BooleanField(default=False)