from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from ..mydb import getColeccion
from ..common.validator import valUserExist, valMessage
from bson.json_util import dumps
import requests
import json


def listTeacherNotes(request):
    if request.method == 'GET':
        coleccion = getColeccion('teachers')
        json_data = []
        error = False
        message = "No se ha calificado a ningun instructor por el momento."
        teacheList = coleccion.find()
        if teacheList.count() != 0:
            for x in teacheList:
                json_data.append(x)
            print("json_data: ", json_data)
            message = "Se retorna el listado de las calificaciones de los instructores."
        returnPeticion = {
            "error": error,
            "message": message,
            "data": json_data
        }
        return JsonResponse(returnPeticion, safe=False)


@csrf_exempt
def inserTeacherNotes(request):
    if request.method == 'POST':
        coleccion = getColeccion('teachers')
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        newTeacherNote = {"student_name": body["student_name"], "student_email": body["student_email"], "student_dni": body["student_dni"], "teacher_name": body["teacher_name"],
                          "teacher_email": body["teacher_email"], "teacher_dni": body["teacher_dni"], "teacher_note": body["teacher_note"], "feedback": body["feedback"]}
        resultInsert = coleccion.insert_one(newTeacherNote).inserted_id
        resultInsert = (0, 1)[resultInsert != None]
        message = valMessage('inserta', 'usuario', resultInsert)
        message = message.replace('la', 'el')
        error = (True, False)[resultInsert != 0]
        returnResponse = {
            "error": error,
            "message": message
        }
        return JsonResponse(returnResponse, safe=False)
