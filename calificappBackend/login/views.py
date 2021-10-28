from django.views.decorators.csrf import csrf_exempt
from ..common.validator import valMessage
from django.http import HttpResponse, JsonResponse
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from ..mydb import getColeccion
from ..common.validator import valUserExist
import requests
import json
import smtplib

bodyCart = "Este correo solo informa que su clave se ha actualizado exitosamente."
subject = 'Cambio de clave'
bodyCart = 'Subject: {}\n\n{}'.format(subject, bodyCart)
server = smtplib.SMTP('smtp.gmail.com', 587)
user = 'cristilopezca@gmail.com'
password = 'linda1208'


@csrf_exempt
def login(request):
    if request.method == 'POST':
        coleccion = getColeccion('users')
        bodyUnicode = request.body.decode('utf-8')
        body = json.loads(bodyUnicode)
        acceso, error, passChange = False, False, False
        message = ''
        userExist = valUserExist(body["user"])
        if userExist != None:
            valUser = coleccion.find_one(
                {'dni': body["user"], 'password': body["password"]})
            if valUser != None:
                acceso = True
                message = 'Usuario autenticado!'
            else:
                message = 'El Usuario o la contraseña no son validos'
        else:
            error = True
            message = 'El usuario no existe en la base de datos'
        if body["user"] == body["password"]:
            passChange = True
        returnPeticion = {
            "error": error,
            "message": message,
            "changePassword": passChange
        }
        return JsonResponse(returnPeticion, safe=False)


@csrf_exempt
def recoverPassword(request):
    if request.method == 'PUT':
        coleccion = getColeccion('users')
        bodyUnicode = request.body.decode('utf-8')
        body = json.loads(bodyUnicode)
        error = True
        message = 'El usuario no existe en la base de datos'
        userExist = valUserExist(body["user"])
        if userExist != None:
            valUser = coleccion.find_one(
                {'dni': body["user"], 'email': body["email"]})
            if valUser != None:
                idFind = {"dni": body["user"]}
                valUser["password"] = body['password']
                resultUpdate = coleccion.update(idFind, valUser)
                print("resultUpdate: ", resultUpdate["nModified"])
                message = valMessage(
                    'actualiza', 'password', resultUpdate["nModified"])
                if resultUpdate["nModified"] == 1:
                    server.starttls()
                    server.login(user, password)
                    server.sendmail(user, body["email"], bodyCart)
                    server.quit()
                    print("Enviado")
                    error = False
        returnPeticion = {
            "error": error,
            "message": message
        }
        return JsonResponse(returnPeticion, safe=False)
