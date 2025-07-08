from django.db import models
from django.utils import timezone
from datetime import datetime
from groups.models import StudentGroup
from services.models import ServiceType

class Lesson(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(editable=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('group', 'date')

    def __str__(self):
        return f"Lesson for {self.group.name} on {self.date}"

    @property
    def teacher(self):
        return self.group.teacher

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            start_dt = datetime.combine(self.date, self.start_time)
            end_dt = datetime.combine(self.date, self.end_time)
            self.duration_minutes = int((end_dt - start_dt).total_seconds() // 60)
        super().save(*args, **kwargs)
