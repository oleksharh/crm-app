from allauth.socialaccount.models import SocialAccount, SocialToken


def get_token_for_user(user) -> SocialToken | None:
    """
    Fetches the SocialToken for a given user.
    Returns a SocialToken object or None if not found.
    """
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
    social_accounts = SocialAccount.objects.filter(user__groups__name__in=role).distinct()

    for account in social_accounts:
        token = SocialToken.objects.filter(account=account).first()
        if token:
            tokens.append(token)

    return tokens


from datetime import datetime, timedelta


def get_today_time_range_iso() -> tuple[str, str]:
    """
    Returns the start and end of the current day in ISO 8601 format with 'Z' suffix.
    """
    time_min = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    time_max = time_min + timedelta(days=1)
    return time_min.isoformat() + 'Z', time_max.isoformat() + 'Z'
