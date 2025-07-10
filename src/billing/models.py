from django.db import models
from django.core.exceptions import ValidationError
from lessons.models import Lesson
from django.contrib.auth.models import User
from decimal import Decimal

class BillingRecord(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="billing_records")
    student_email = models.EmailField()
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name__in": ["student"]},
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    issued_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("lesson", "student_email")

    def __str__(self):
        return f"Billing for {self.student_email} in {self.lesson}"

    def clean(self):
        # Import locally to avoid circular imports
        from groups.models import GroupMember

        group = self.lesson.group
        member_exists = GroupMember.objects.filter(
            group=group,
            email__iexact=self.student_email
        ).exists()

        if not member_exists:
            raise ValidationError(f"{self.student_email} is not in the group '{group.name}'.")


    # TODO: CHANGE THIS To a seperate form/service not to get null problems
    # NOTE: THIS IS BAD Practice
    def save(self, *args, **kwargs):
        # Always get current price from the lesson's service type
        if not self.amount:
            self.amount = self.lesson.service_type.base_price or Decimal("0.00")
        self.full_clean()
        
        if not self.student:
            # If student is not provided, try to find by email
            try:
                self.student = User.objects.get(email=self.student_email)
            except User.DoesNotExist:
                self.student = None
        
        super().save(*args, **kwargs)
