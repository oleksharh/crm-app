from django.db import models
from lessons.models import Lesson
from django.contrib.auth.models import User
from users.models import StudentProfile



class GroupBillingRecord(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    month = models.DateField()  # Represents the month for which the invoice is issued
    issued_at = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField() # Number of lessons completed at the end of the month
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_per_student = models.DecimalField(max_digits=10, decimal_places=2)
    student_count = models.PositiveIntegerField()


class StudentPaymentStatus(models.Model):
    group_billing = models.ForeignKey(GroupBillingRecord, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
