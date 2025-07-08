from django.db import models
from django.contrib.auth.models import User

class StudentGroup(models.Model): # Works as general Lesson Group
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name__in": ["teacher", "principal"]},
    )
    created_at = models.DateField()
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    


    class Meta:
        unique_together = ("name", "teacher")
    

    def __str__(self):
        return f"{self.name}"
    
    
class GroupMember(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name__in": ["student"]},
        null=True,
        blank=True,
    )
    email = models.EmailField(null=False, blank=False, unique=True) # This field is required
    joined_date = models.DateField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.student and self.email:
            # If student is not provided, try to find by email
            try:
                self.student = User.objects.get(email=self.email)
            except User.DoesNotExist:
                self.student = None
        elif self.student and not self.email:
            # If student is provided, ensure email is set
            self.email = self.student.email
            
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.email} in {self.group.name}"
    
    