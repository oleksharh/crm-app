from django.contrib import admin
from .models import ServiceType, TeacherServiceRate
from django.urls import path
from django.http import JsonResponse

admin.site.register(TeacherServiceRate)
admin.site.register(ServiceType)
