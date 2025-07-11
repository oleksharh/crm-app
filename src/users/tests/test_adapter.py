# TODO: This test needs to be adapted to the improved adapter logic

import pytest
from django.contrib.auth.models import User
from users.adapter import CustomAccountAdapter
from rolepermissions.roles import assign_role


class DummyRequest:
    def __init__(self, user):
        self.user = user
        self.META = {'HTTP_REFERER': ''}
        self.path = '/'


@pytest.mark.django_db
def test_get_login_redirect_url_student(client):
    user = User.objects.create_user(username='stu', email='stu@example.com')
    assign_role(user, 'student')
    client.force_login(user)
    adapter = CustomAccountAdapter()

    assert adapter.get_login_redirect_url(DummyRequest(user)) == '/dashboard/student/'


# @pytest.mark.django_db
# def test_get_login_redirect_url_unrecognized_role(client):
#     user = User.objects.create_user(username='weird', email='weird@example.com')
#     client.force_login(user)
#     adapter = CustomAccountAdapter()
#
#     assert adapter.get_login_redirect_url(DummyRequest(user)) == '/unknown/name/of/the/page/yet'
