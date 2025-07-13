from traceback import print_tb

from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver
from rolepermissions.roles import assign_role
from django.contrib.auth.models import User
from .models import ApprovedUser, StudentProfile


@receiver(user_signed_up)
def assign_role_after_google_signup(request, user, **kwargs):
    # Assigning roles only to users who signed up via Google
    if 'sociallogin' not in kwargs:
        return

    email = user.email.lower()

    approved_user_roles = ApprovedUser.objects.filter(email=email)

    if approved_user_roles:
        for approved_user in approved_user_roles:
            user.is_active = True
            user.save()
            assign_role(user, approved_user.role.name)

            # Delete the ApprovedUser instance after assigning the role
            approved_user.delete()

    else:
        user.is_active = False
        user.save()
        # NOTE: maybe send email to admin about unapproved user


@receiver(post_save, sender=User)
def create_or_update_student_profile_for_user(sender, instance, created, **kwargs):
    if StudentProfile.objects.filter(user=instance).exists():
        return

    try:
        profile = StudentProfile.objects.get(email=instance.email, user__isnull=True)
        profile.user = instance
        profile.save()
    except StudentProfile.DoesNotExist:
        StudentProfile.objects.get_or_create(user=instance, defaults={"email": instance.email})


@receiver(post_save, sender=ApprovedUser)
def create_or_update_student_profile_for_approved_user(sender, instance, created, **kwargs):
    StudentProfile.objects.get_or_create(email=instance.email)
