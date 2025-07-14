from django.db import models
from pytz import timezone as tzlib
from groups.models import StudentGroup
from services.models import ServiceType


class Lesson(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=False, blank=False)
    start_utc = models.DateTimeField()
    duration = models.DurationField()
    timezone = models.CharField(max_length=64)  # Just for reference and future lookups, start already has timezone info
    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="scheduled",
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("group", "start_utc")
        indexes = [
            models.Index(fields=["start_utc"]),
        ]

    def __str__(self):
        return f"Lesson for {self.group.name} on UTC: {self.utc_date} on local: {self.local_date}"


    @property
    def teacher(self):
        return self.group.teacher

    @property
    def name(self):
        return self.group.name

    @property
    def utc_date(self):
        return self.start_utc.date()

    @property
    def local_date(self):
        if self.timezone == "Unknown":
            return "Unknown"
        return self.start_utc.astimezone(tzlib(self.timezone)).date()

    @property
    def end(self):
        return self.start_utc + self.duration

