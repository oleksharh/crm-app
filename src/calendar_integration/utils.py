from datetime import datetime, timedelta
import json
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def connect_to_calendar(token):
    app = SocialApp.objects.get(provider='google')

    # Finally making a connection request
    creds = Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=app.client_id,
        client_secret=app.secret,
        scopes=[
            "https://www.googleapis.com/auth/calendar"
        ],
    )
    service = build('calendar', 'v3', credentials=creds)
    return service


def fetch_user_calendar_events(token, time_min, time_max):
    """Fetches events from the user's calendar using the provided access token."""
    service = connect_to_calendar(token)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])


def connect_to_calendar_for_user(request):
    # Fetches the User of the request
    qs = SocialAccount.objects.filter(user=request.user)
    print(qs)
    # Fetches the Access token of the User
    token = SocialToken.objects.filter(account=qs[0])
    app = SocialApp.objects.get(provider='google')

    token = token[0]
    # Finally making a connection request
    creds = Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=app.client_id,
        client_secret=app.secret,
        scopes=[
            "https://www.googleapis.com/auth/calendar"
        ],
    )
    service = build('calendar', 'v3', credentials=creds)
    return service

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
