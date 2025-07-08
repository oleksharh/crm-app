from django.contrib import admin
from .models import StudentGroup, GroupMember

admin.site.register(StudentGroup)
admin.site.register(GroupMember)