from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class ApprovedUser(models.Model):
    email = models.EmailField(verbose_name="Email Address")
    role = models.ForeignKey(Group, verbose_name="Role", on_delete=models.PROTECT)

    class Meta:
        unique_together = ('email', 'role')

    def __str__(self):
        return f"{self.email} - {self.role.name}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(verbose_name="Email Address", null=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name="Full Name", blank=True, null=True)

    def __str__(self):
        if self.user:
            return f"{self.user.email} - {self.user.first_name} {self.user.last_name}"

        if self.email:
            return f"{self.email} - {self.full_name or 'No Name'}"