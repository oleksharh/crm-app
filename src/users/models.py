from django.db import models


class TeacherWhiteList(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    
    def __str__(self):
        return self.email