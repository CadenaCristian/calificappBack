from django.urls import path
from .views import listTeachers, createUser, findUserById, updateUser, deleteUser

urlpatterns = [
    path('listTeachers', listTeachers),
    path('createUser', createUser),
    path('findUserById/<int:dni>', findUserById),
    path('updateUser', updateUser),
    path('deleteUser/<int:dni>', deleteUser)
]
