import configparser

from mongoengine import connect


config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('mongo', 'USER')
password = config.get('mongo', 'PASSWORD')
database_name = config.get('mongo', 'DB_NAME')
domain = config.get('mongo', 'DOMAIN')

uri = f"mongodb+srv://{username}:{password}@{domain}/{database_name}?retryWrites=true&w=majority"
# url = f'mongodb+srv://{username}:{password}@{domain}/{database_name}?retryWrites=true&w=majority'

try:
    m_connect = connect(host=uri, ssl=True)
except:
    print('Connection to database failed')
    quit()





