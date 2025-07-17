from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import User

# FIXME: Improvement: Add select_related("user") in SocialAccount.objects.get(...) to reduce DB hits
#  if accessing user later.
# NOTE:❗Security note: You might want to restrict token access to only active users or filter on roles more
#  defensively (user__is_active=True).

def get_token_for_user(user) -> SocialToken | None:
    """
    Fetches the SocialToken for a given user.
    Returns a SocialToken object or None if not found.
    """
    if not isinstance(user, User):
        raise ValueError("The provided user must be an instance of django User model")

    if not user.is_active:
        return None

    try:
        social_account = SocialAccount.objects.get(user=user)
        token = SocialToken.objects.get(account=social_account)
        return token
    except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
        return None


def get_tokens_by_role(role: str | list[str]) -> list[SocialToken]:
    """
    Fetches all SocialTokens for users with a specific role.
    Returns a list of SocialToken objects.
    """
    if isinstance(role, str):
        role = [role]

    tokens = []
    social_accounts = SocialAccount.objects.filter(user__groups__name__in=role).distinct() #TODO:

    for account in social_accounts:
        token = SocialToken.objects.filter(account=account).first()
        if token:
            tokens.append(token)

    return tokens