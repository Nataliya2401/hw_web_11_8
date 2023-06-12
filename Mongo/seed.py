import json
from pathlib import Path
from pprint import pprint
from mongoengine.errors import NotUniqueError, DoesNotExist
from models import Author, Quotes
import connect

BASE_DIR = Path()
STORAGE_PATH = BASE_DIR.joinpath('storage')
STORAGE_AUTHORS = STORAGE_PATH / 'authors.json'
STORAGE_QUOTES = STORAGE_PATH / 'quotes.json'


def load_data_to_db(storage_file):
    with open(storage_file, "r", encoding='utf-8') as f:
        res = json.load(f)
        return res


def add_authors_db():
    Author.drop_collection()
    res = load_data_to_db(STORAGE_AUTHORS)

    for el in res:
        try:
            author = Author(fullname=el['fullname'],
                            born_date=el["born_date"],
                            born_location=el["born_location"],
                            description=el["description"]).save()
            # print(author.to_mongo().to_dict())
        except NotUniqueError as err:
            print("this author", el["fullname"], 'is already in DB')
            pass
    return author


def add_quotes_db():
    Quotes.drop_collection()
    res = load_data_to_db(STORAGE_QUOTES)

    for el in res:
        print(el["author"])
        try:
            author = Author.objects.get(fullname=el["author"])
            quote = Quotes(tags=el["tags"],
                           author=author.id,
                           quote=el["quote"])
            quote.save()
        except DoesNotExist as err:
            print("Author ",  el["author"],  " not found. Quote didn't add:")
            print(el)
            pass


def add_quotes():
    Quotes.drop_collection()

    # quotes = []
    quotes = load_data_to_db(STORAGE_QUOTES)

    for el in quotes:
        author = Author.objects.get(fullname=el['author'])
        if not author:
            print('---------------------------------------------------------')
            print('Author', el['author'], 'not found')
            print(" Quote didn't add: ")
            print(el)
            print('---------------------------------------------------------')
        else:
            quote = Quotes(
                tags=el['tags'],
                author=author,
                quote=el['quote']
            )
            quote.save()


if __name__ == '__main__':
    add_authors_db()
    add_quotes_db()





