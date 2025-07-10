from django.contrib.auth.decorators import login_required
from rolepermissions.checkers import has_role
from rolepermissions.decorators import has_role_decorator

from .utils import fetch_user_calendar_events



def fetch_event(request):
    """
    Fetches events from the user's calendar.
    Only accessible to users with 'teacher' or 'principal' roles.
    """
