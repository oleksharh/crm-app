from django.db import models
from django.contrib.auth.models import Group

from rolepermissions import roles




class ApprovedUser(models.Model):
    email = models.EmailField(verbose_name="Email Address")
    role = models.ForeignKey(Group, verbose_name="Role", on_delete=models.PROTECT)

    class Meta:
        unique_together = ('email', 'role')


    def __str__(self):
        return f"{self.email} - {self.role.name}"


# class ApprovedTeacher(models.Model):
#     email = models.EmailField(unique=True, verbose_name="Email Address")
#
#     def __str__(self):
#         return self.email