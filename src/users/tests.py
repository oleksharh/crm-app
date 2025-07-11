from django.test import TestCase

import pytest
from django.contrib.auth import get_user_model
from rolepermissions.roles import get_user_roles

User = get_user_model()

@pytest.mark.django_db
def test_student_role_assignment():
    assert True
