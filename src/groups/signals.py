from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GroupMember
from users.models import ApprovedStudent

@receiver(post_save, sender=GroupMember)
def sync_email_to_other_model(sender, instance, created, **kwargs):
    email = instance.email

    ApprovedStudent.objects.update_or_create(email=email)
