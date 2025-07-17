from datetime import datetime, timedelta
import json

from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# def _connect_to_calendar(token: SocialToken, app: SocialApp):
#     """
#     Internal helper to create a Google Calendar API service using a SocialToken and SocialApp.
#     """
#     creds = Credentials(
#         token=token.token,
#         refresh_token=token.token_secret,
#         token_uri="https://oauth2.googleapis.com/token",
#         client_id=app.client_id,
#         client_secret=app.secret,
#         scopes=[
#             "https://www.googleapis.com/auth/calendar"
#         ],
#     )
#     return build('calendar', 'v3', credentials=creds)
#
#
# def connect_to_calendar_for_user(request, user: User = None):
#     """
#     Connects to Google Calendar for the authenticated user in the request.
#     """
#     if user is None:
#         user = request.user
#
#     try:
#         app = SocialApp.objects.get(provider='google')
#     except SocialApp.DoesNotExist:
#         raise ValueError("Google SocialApp not found. Please configure it in the admin panel.")
#
#     qs = SocialAccount.objects.filter(user=user)
#     if not qs.exists():
#         raise ValueError("No social account found for user.")
#     token_qs = SocialToken.objects.filter(account=qs[0])
#     if not token_qs.exists():
#         raise ValueError("No social token found for user.")
#
#     return _connect_to_calendar(token_qs[0], app)
#
#
# def connect_to_calendar_by_token(token: SocialToken):
#     try:
#         app = SocialApp.objects.get(provider='google')
#     except SocialApp.DoesNotExist:
#         raise ValueError("Google SocialApp not found. Please configure it in the admin panel.")
#     return _connect_to_calendar(token, app)


# def fetch_user_calendar_events_by_token(token, time_min, time_max) -> list[dict]:
#     """Fetches events from the user's calendar using the provided access token."""
#     service = connect_to_calendar_by_token(token)
#
#     events_result = service.events().list(
#         calendarId='primary',
#         timeMin=time_min,
#         timeMax=time_max,
#         singleEvents=True,
#         orderBy='startTime'
#     ).execute()
#
#     return events_result.get('items', [])





# import json
# from django.contrib.auth.decorators import login_required
# from rolepermissions.decorators import has_role_decorator
#
# from calendar_sync.time.ranges import get_today_time_range_tz_aware_iso
# from .tokens import get_token_for_user
# from .parser import get_parsed_event_object
# from calendar_sync.db.lessons import create_or_update_lesson
#
# @login_required
# @has_role_decorator(["teacher", "principal"])  # inside it uses has_role(user, roles: list[str])
# def fetch_events_for_day(request) -> dict:
#     user = request.user
#     token = get_token_for_user(user)
#
#     if not token:
#         return {"error": "No calendar token found for the user."}
#
#     user_tz = user.tz_profile.timezone
#
#     if not user_tz:
#         raise PermissionError("No time zone found for the user.")
#
#     min_time, max_time = get_today_time_range_tz_aware_iso(user_tz)
#
#     user_events = fetch_user_calendar_events_by_token(token, min_time, max_time)
#
#     if not user_events:
#         return {"error": "No events found for the user."}
#
#     events_data_status = []
#     for event in user_events:
#         parsed_event = get_parsed_event_object(event)
#         event_added = create_or_update_lesson(parsed_event)
#         events_data_status.append(event_added)
#
#     return {"events": events_data_status}



















# NOTE: Everything below this line is not used in the current implementation but might be useful in the future.


# This function accept comma separated string of email like "moinkhan8439@gmail.com , shahfahadkhan3@gmail.com "
# and returns a list of dictionary in the format : [ {'email' : 'moinkhan8439@gmail.com'} , {'email' : 'shahfahadkhan3@gmail.com' }]
def convert_attendees_to_list(attendees):
    res = list()
    for i in attendees.split(','):
        d = dict()
        d['email'] = i.strip()
        res.append(d)
    return res


'''    
#This function is to be used if we use quickadd to add events 
def convert_date(date1,date2):
    if(date1.day == date2.day ):
        s=f'{date1.strftime("%B")} {str(date1.day)} {str(date1.hour)}:{str(date1.minute)} - {str(date2.hour)}:{str(date2.minute)}'
    else:
        s=f' {str(date1.day)}/{str(date1.month)} - {str(date2.day)}/{str(date2.month)}'
    return s
'''


# This function convert date into 2021-03-22T00:40:00+05:30
def convert_RFC(date):
    return str(date.isoformat('T'))


def prepare_event(data):
    start = convert_RFC(data["start_time"])
    end = convert_RFC(data["end_time"])
    email = convert_attendees_to_list(data['attendees'])
    event = {
        'summary': data["summary"],
        'description': data["description"],
        'start': {
            'dateTime': start,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': email,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        }
    }
    return event

