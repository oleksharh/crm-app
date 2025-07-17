from traceback import print_tb

from allauth.account.signals import user_signed_up, user_logged_in
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



from .models import UserProfileTZ
from calendar_sync.time.conversions import get_user_timezone_from_google
from calendar_sync.google.tokens import get_token_for_user

@receiver(user_logged_in)
def set_user_timezone_after_login(request, user, **kwargs):
    """
    Set the user's timezone after they log in.
    This assumes you have a function to fetch the timezone from Google Calendar.
    """
    if not user.socialaccount_set.filter(provider='google').exists():
        raise "User does not have a Google social account associated."

    try:
        token = get_token_for_user(user)


        timezone = get_user_timezone_from_google(token.token)
        UserProfileTZ.objects.update_or_create(user=user, defaults={'timezone': timezone})
    except Exception as e:
        raise f"Failed to set timezone for user {user.email}: {str(e)}"