import pytest
from django.contrib.auth.models import User, Group
from allauth.account.signals import user_signed_up
from users.models import ApprovedUser
from users.signals import assign_role_after_google_signup
from django.test.client import RequestFactory


@pytest.mark.django_db
def test_role_assignment_signal_assigns_role(mocker):
    factory = RequestFactory()
    request = factory.post('/accounts/social/signup/')

    group = Group.objects.create(name='teacher')
    ApprovedUser.objects.create(email='approved@example.com', role=group)

    user = User.objects.create_user(username='approved', email='approved@example.com')

    mock_assign = mocker.patch('users.signals.assign_role')

    mock_sociallogin = mocker.Mock()
    user_signed_up.send(
        sender=User,
        request=request,
        user=user,
        sociallogin=mock_sociallogin  # simulate Google OAuth
    )

    user.refresh_from_db()
    assert user.is_active is True
    mock_assign.assert_called_once_with(user, 'teacher')
    assert not ApprovedUser.objects.filter(email='approved@example.com').exists()


@pytest.mark.django_db
def test_role_assignment_signal_rejects_unapproved(mocker):
    factory = RequestFactory()
    request = factory.post('/accounts/social/signup/')

    user = User.objects.create_user(username='unknown', email='notapproved@example.com')

    mock_sociallogin = mocker.Mock()
    user_signed_up.send(
        sender=User,
        request=request,
        user=user,
        sociallogin=mock_sociallogin  # simulate Google OAuth
    )

    user.refresh_from_db()
    assert user.is_active is False
