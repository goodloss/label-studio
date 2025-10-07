from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WkoicdConfig(AppConfig):
    name = "wkoicd"
    verbose_name = _("wkoicd")
    default_auto_field = "django.db.models.AutoField"
    print(">>>>>>>>>>>>>>", AppConfig)
