import pymongo

cluster = pymongo.MongoClient(
    'mongodb://admin:admin@calificapp-shard-00-00.bxej7.mongodb.net:27017,calificapp-shard-00-01.bxej7.mongodb.net:27017,calificapp-shard-00-02.bxej7.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-mfbpf9-shard-0&authSource=admin&retryWrites=true&w=majority')
# &connectTimeoutMS=60000

db = cluster["CalificAPP"]


def getColeccion(name):
    coleccion = db[name]
    return coleccion
