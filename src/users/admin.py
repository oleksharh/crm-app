from django.contrib import admin
from .models import ApprovedTeacher, ApprovedStudent

admin.site.register(ApprovedTeacher)
admin.site.register(ApprovedStudent)