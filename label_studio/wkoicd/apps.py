from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "wkoicd"
    verbose_name = _("WKUsers")
    default_auto_field = "django.db.models.AutoField"
