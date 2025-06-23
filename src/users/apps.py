from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


# TODO: Research how to properly implement for the production environment
    # def ready(self):
    #     from allauth.socialaccount.models import SocialApp
    #     from django.contrib.sites.models import Site

    #     if not SocialApp.objects.filter(provider='google').exists():
    #         app = SocialApp.objects.create(
    #             provider='google',
    #             name='Google',
    #             client_id=settings.GOOGLE_CLIENT_ID,
    #             secret=settings.GOOGLE_CLIENT_SECRET,
    #         )
    #         app.sites.add(Site.objects.get_current())
    
#     C:\Projects\crm-app\crm-venv\Lib\site-packages\django\db\backends\utils.py:98: RuntimeWarning: Accessing the database during app initialization is discouraged. To fix this warning, avoid executing queries in AppConfig.ready() or when your app modules are imported.
#   warnings.warn(self.APPS_NOT_READY_WARNING_MSG, category=RuntimeWarning)
# C:\Projects\crm-app\crm-venv\Lib\site-packages\django\db\backends\utils.py:98: RuntimeWarning: Accessing the database during app initialization is discouraged. To fix this warning, avoid executing queries in AppConfig.ready() or when your app modules are imported.
#   warnings.warn(self.APPS_NOT_READY_WARNING_MSG, category=RuntimeWarning)