from pymongo import MongoClient

mongodb = None


def init_db(config):
    global mongodb
    host, username, password, port = [config[_] for _ in ['HOST', 'USERNAME', 'PASSWORD','PORT']]
    mongodb = MongoClient(host=host, username=username, password=password, port=int(port))


def get_db():
    return mongodb["python-authent-service"]
