from django.db import models
from django.contrib.auth.models import User
from services.models import ServiceType
from users.models import StudentProfile


class StudentGroup(models.Model):  # Works as general Lesson Group
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name__in": ["teacher", "principal"]},
    )
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    created_at = models.DateField()
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("name", "teacher")

    def clean(self):
        super().clean()
        # TODO: Add validation of the teachr and name checked agains google calendar
        # params, that are: creator.email = teacher.email, summary = name

    def __str__(self):
        return f"{self.name} - {self.teacher.first_name} {self.teacher.last_name} ({self.teacher.email})"


class GroupMember(models.Model):
    group = models.ForeignKey(
        StudentGroup, on_delete=models.CASCADE, related_name="members"
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True)
    joined_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.student.email} in {self.group.name}"
