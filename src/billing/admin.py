from django.contrib import admin
from .models import GroupBillingRecord, StudentPaymentStatus

admin.site.register(GroupBillingRecord)
admin.site.register(StudentPaymentStatus)