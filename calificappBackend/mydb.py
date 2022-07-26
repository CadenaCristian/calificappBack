import pymongo


cluster = pymongo.MongoClient(
    "mongodb+srv://cristian:Linda1208@calificapp.bxej7.mongodb.net/?retryWrites=true&w=majority")
# &connectTimeoutMS=60000

db = cluster["CalificAPP"]


def getColeccion(name):
    coleccion = db[name]
    return coleccion
