from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from rolepermissions.roles import assign_role
from .models import ApprovedUser


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
