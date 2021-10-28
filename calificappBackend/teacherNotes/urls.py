from django.urls import path
from .views import listTeacherNotes, inserTeacherNotes

urlpatterns = [
    path('listTeacherNotes', listTeacherNotes),
    path('inserTeacherNotes', inserTeacherNotes)
]
