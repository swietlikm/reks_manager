from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "reks_manager.user_auth"
    verbose_name = _("User-Auth")

    #
    # def ready(self):
    #     try:
    #         import reks_manager.users.signals  # noqa: F401
    #     except ImportError:
    #         pass
