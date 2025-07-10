from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GroupMember
from users.models import ApprovedUser


@receiver(post_save, sender=GroupMember)
def sync_email_to_other_model(sender, instance, created, **kwargs):
    if not instance:
        raise (ValueError(f"Instance is None: {instance}"))

    ApprovedUser.objects.update_or_create(email=instance.email, role=instance.role)
