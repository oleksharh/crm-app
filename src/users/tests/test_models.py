import pytest
from django.contrib.auth.models import User, Group
from users.models import ApprovedUser, StudentProfile


@pytest.mark.django_db
def test_approved_user_str():
    group = Group.objects.create(name='teacher')
    approved = ApprovedUser.objects.create(email='test@example.com', role=group)
    assert str(approved) == 'test@example.com - teacher'


@pytest.mark.django_db
def test_student_profile_str_with_user():
    user = User.objects.create_user(username='john', email='john@example.com', first_name='John', last_name='Doe')
    profile = StudentProfile.objects.create(user=user)
    assert str(profile) == 'john@example.com - John Doe'


@pytest.mark.django_db
def test_student_profile_str_with_email_and_name():
    profile = StudentProfile.objects.create(email='anon@example.com', full_name='Jane Doe')
    assert str(profile) == 'anon@example.com - Jane Doe'


@pytest.mark.django_db
def test_student_profile_str_with_email_only():
    profile = StudentProfile.objects.create(email='anon@example.com')
    assert str(profile) == 'anon@example.com - No Name'