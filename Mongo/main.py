import re
from pprint import pprint
from models import Author, Quotes
import redis
from redis_lru import RedisLRU
import connect

client = redis.StrictRedis(host="localhost", port=6379, password=None, charset="utf-8")
cache = RedisLRU(client)


@cache
def find_by_author(name):
    print("For test - cache - call find_by_author")
    quotes = {}
    list_quote = []
    author = Author.objects(fullname__istartswith=name)
    if not author:
        print("Author not found")
    else:
        for a in author:
            quote = Quotes.objects(author=a)
            if not quote:
                print("Quote not found")
            else:
                for q in quote:
                    list_quote.append(q.quote)
                quotes[a.fullname] = list_quote
    return quotes


@cache
def find_by_tag(tag):
    expr = re.compile(f'.*{tag}.*')
    # quotes = {}
    list_quote = []
    quote = Quotes.objects(tags=expr)
    if not quote:
        print(f'For {tag} quotes not found')
    else:
        for q in quote:
            quote_str = f'for {tag} quotes: {q.quote} . Author - {q.author.fullname}'
            list_quote.append(quote_str)
        # quotes[tag] = list_quote
    return list_quote


@cache
def find_by_tags(tags):
    answers = {}
    list_tags = tags.split(',')
    for t in list_tags:
        answer = find_by_tag(t)
        answers[t] = answer
    return answers


def goodbye():
    print('Goodbye!')
    quit()


def help_func():
    print("Examples of queries:")
    print('name:St — quotes of Steve Martin')
    print('tag:li — quotes for teg life or live')
    print('tags:li,mi -- quotes for tegs life or live or mirracle...')
    print('exit - for exit')


COMMANDS = {"name": find_by_author,
            "tag": find_by_tag,
            "tags": find_by_tags,
            "help": help_func,
            "exit": goodbye
            }


def main():
    while True:
        cmd = input("Enter one of the commands:'name':<value>,'tag':<value>,'tags':<value> or 'exit' : ")
        commands = cmd.split(':')
        if not commands or commands[0] not in COMMANDS:
            print('Wrong command. Try again or input "exit"')
        else:
            if len(commands) == 1:
                COMMANDS[commands[0]]()
            else:
                answer = COMMANDS[commands[0]](commands[1])
                pprint(answer)


if __name__ == '__main__':
    main()
