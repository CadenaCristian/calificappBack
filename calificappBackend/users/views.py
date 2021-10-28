from email import message
from typing import Collection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from ..mydb import getColeccion
from ..common.validator import valUserExist, valMessage
from bson.json_util import dumps
import requests
import json


@csrf_exempt
def listTeachers(request):
    if request.method == 'GET':
        coleccion = getColeccion('users')
        json_data = []
        error = False
        message = "No se han ingresado instructores por el momento."
        teacheList = coleccion.find(
            {'rol': 'teacher'}, {'_id': 0, 'name': 1, 'rol': 1, 'email': 1, 'dni': 1})
        if teacheList.count() != 0:
            for x in teacheList:
                json_data.append(x)
            message = "Se retorna el listado de instructores."
        returnPeticion = {
            "error": error,
            "message": message,
            "data": json_data
        }
        return JsonResponse(returnPeticion, safe=False)


@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        coleccion = getColeccion('users')
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        error = True
        newUser = {'name': body["name"], 'rol': body["rol"], 'email': body["email"],
                   'dni': body["dni"], 'password': body["password"]}
        userExist = valUserExist(body["dni"])
        if userExist != None:
            message = "El usuario ya existe, por favor validar la cedula"
        else:
            resultUpdate = coleccion.insert_one(newUser).inserted_id
            resultUpdate = (0, 1)[resultUpdate != None]
            message = valMessage('inserta', 'usuario', resultUpdate)
            message = message.replace('la', 'el')
            error = False
        returnResponse = {
            "error": error,
            "message": message
        }
        return JsonResponse(returnResponse, safe=False)


@csrf_exempt
def findUserById(request, dni):
    if request.method == 'GET':
        coleccion = getColeccion('users')
        error = True
        message = "No coincide esa cedula con la de ningun usuario."
        dataUser = coleccion.find_one(
            {'dni': str(dni)}, {'rol': 0, '_id': 0, 'name': 1, 'rol': 1, 'email': 1, 'dni': 1})
        if dataUser != None:
            error = False
            message = "Se retornan los datos del usuario"
        returnResponse = {
            "error": error,
            "message": message,
            "data": dumps(dataUser)
        }
        return JsonResponse(returnResponse, safe=False)


@csrf_exempt
def updateUser(request):
    if request.method == 'PUT':
        coleccion = getColeccion('users')
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        error = True
        idFind = {"dni": str(body["dni"])}
        newValue = {"name": body["name"], "rol": body["rol"],
                    "email": body["email"], "dni": body["dni"], "password": body["password"]}
        resultUpdate = coleccion.update(idFind, newValue)
        message = valMessage('actualiza', 'usuario', resultUpdate["nModified"])
        message = message.replace('la', 'el')
        error = (False, True)[resultUpdate["nModified"] == 0]
        returnResponse = {
            "error": error,
            "message": message
        }
        return JsonResponse(returnResponse, safe=False)


@csrf_exempt
def deleteUser(request, dni):
    if request.method == 'DELETE':
        coleccion = getColeccion('users')
        dniUser = {"dni": str(dni)}
        resultDelete = coleccion.delete_one(dniUser)
        message = valMessage('elimina', 'usuario', resultDelete.deleted_count)
        message = message.replace('la', 'el')
        returnResponse = {
            "error": "prueba",
            "message": message
        }
        return JsonResponse(returnResponse, safe=False)
