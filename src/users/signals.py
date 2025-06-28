from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from rolepermissions.roles import assign_role
from .models import ApprovedStudent, ApprovedTeacher

@receiver(user_signed_up)
def assign_role_after_google_signup(request, user, **kwargs):
    email = user.email.lower()

    if ApprovedStudent.objects.filter(email=email).exists():
        assign_role(user, 'student')
        # NOTE: maybe link profile or mark as claimed
        
    elif ApprovedTeacher.objects.filter(email=email).exists():
        assign_role(user, 'teacher')
    else:
        user.is_active = False
        user.save()
        # NOTE: maybe send email to admin about unapproved user
        