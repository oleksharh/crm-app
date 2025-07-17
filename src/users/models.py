from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ApprovedUser(models.Model):
    email = models.EmailField(verbose_name="Email Address")
    role = models.ForeignKey(Group, verbose_name="Role", on_delete=models.PROTECT)

    class Meta:
        unique_together = ('email', 'role')

    def clean(self):
        self.email = self.email.lower()

        if not Group.objects.filter(id=self.role.id).exists():
            raise ValidationError("The specified role does not exist.")

        if User.objects.filter(email=self.email).exists():
            raise ValidationError("A user with this email already exists.")
        super().clean()

    def __str__(self):
        return f"{self.email} - {self.role.name}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(verbose_name="Email Address", null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.email} - {self.user.first_name} {self.user.last_name}"

        if self.email:
            return f"{self.email} - No Name"


class UserProfileTZ(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tz_profile')
    timezone = models.CharField(max_length=64, default='UTC')

    def __str__(self):
        return f"{self.user.email} - {self.timezone}"

    class Meta:
        verbose_name = "User Timezone"
        verbose_name_plural = "User Timezones"

