from ..mydb import getColeccion


def valUserExist(data):
    coleccion = getColeccion('users')
    exist = coleccion.find_one({'dni': data})
    return exist


def valMessage(crudMessage, word, boolRequest):
    success = 'Se {} la {} exitosamente!'.format(crudMessage, word)
    error = 'fallo al {} la {}.'.format(crudMessage, word)
    return success if boolRequest == 1 else error
