from django.db import models
from groups.models import StudentGroup
from django.contrib.auth.models import User
from users.models import StudentProfile



class GroupBillingRecord(models.Model):
    """
    Represents a monthly billing record for a group lesson, issued at the end of each month.
    """
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    issued_at = models.DateField(auto_now_add=True)
    month = models.DateField()  # Represents the month for which the invoice is issued
    quantity = models.PositiveIntegerField() # Number of lessons completed at the end of the month
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_per_student = models.DecimalField(max_digits=10, decimal_places=2)
    student_count = models.PositiveIntegerField()

    # TODO: Make sure if this field is necessary, as paid status can be tracked through StudentPaymentStatus
    paid = models.BooleanField(default=False, help_text='Paid status of the billing record')

    class Meta:
        unique_together = ('group', 'issued_at') # Avoiding duplicates for the same lesson and month and year

    def __str__(self):
        return f"Billing Record for {self.group} - {self.month.strftime('%B %Y')} (Issued: {self.issued_at})"


class StudentPaymentStatus(models.Model):
    """
    Represents the payment status of a student in the group lesson billing record.
    """
    group_billing = models.ForeignKey(GroupBillingRecord, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('group_billing', 'student')


    def __str__(self):
        return f"Payment Status for {self.student} in {self.group_billing} - {'Paid' if self.paid else 'Unpaid'}"