from django.urls import path
from .views import login, recoverPassword

urlpatterns = [
    path('login', login),
    path('recoverPassword', recoverPassword)
]
