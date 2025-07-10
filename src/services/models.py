from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("jp", "Japanese"),
    ("de", "German"),
]

AGE_GROUP_CHOICES = [
    ("child", "Child"),
    ("teen", "Teenager"),
    ("adult", "Adult"),
]

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    code = models.SlugField(unique=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("language", "age_group", "code")

    def __str__(self):
        return f"{self.name} ({self.language} - {self.age_group})"


class TeacherServiceRate(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name__in": ["teacher", "principal"]},
    )
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    percentage = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter an integer percentage between 0 and 100",
    )
    teacher_share = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    principal_share = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def clean(self):
        super().clean()
        if (self.percentage is None and self.teacher_share is None) or \
           (self.percentage is not None and self.teacher_share is not None):
            raise ValidationError("You must provide either percentage or teacher_share, not both or neither.")

        if self.teacher_share is not None and self.teacher_share > self.service_type.base_price:
            raise ValidationError({
                'teacher_share': f"Teacher share cannot exceed base price ({self.service_type.base_price})."
            })


    # TODO: If someone manually sets teacher_share, then .save()
    # will still recompute based on percentage (even if it’s no longer intended).
    # This overwrites user input silently.
    def calculate_payouts(self):
        if self.percentage is not None:
            self.teacher_share = (self.service_type.base_price * self.percentage) / 100
        # else teacher_share is manually provided, use as is
        
        if self.teacher_share is None:
            self.teacher_share = 0

        self.principal_share = self.service_type.base_price - self.teacher_share

    def save(self, *args, **kwargs):
        self.calculate_payouts()
        super().save(*args, **kwargs)
