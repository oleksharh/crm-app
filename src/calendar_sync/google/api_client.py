import logging

from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.contrib.auth.models import User


# TODO: Check if the Google OAuth token is expired before using it.
#  If expired, refresh the token using google.oauth2.credentials.Credentials.
#  Save the refreshed token and its expiration back to the SocialToken model.
def _check_social_app_exists(provider: str) -> SocialApp:
    try:
        return SocialApp.objects.get(provider=provider)
    except SocialApp.DoesNotExist:
        raise Exception(f'{provider} SocialApp not found, Please configure it in the admin panel')


def build_calendar_service(token: SocialToken):
    app = _check_social_app_exists('google')

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

    return build('calendar', 'v3', credentials=creds)


def build_calendar_service_by_user(user: User):
    try:
        user_account = SocialAccount.objects.get(user=user, provider='google')
        token = SocialToken.objects.get(account=user_account)
    except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
        raise Exception("No social account or token found for user.")

    return build_calendar_service(token)
