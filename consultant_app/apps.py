from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _



class ConsultantAppConfig(AppConfig):
    name = 'consultant_app'

    # def ready(self):
    #     import consultant_app.signals


# class ProfilesConfig(AppConfig):
#     name = 'cmdbox.profiles'
#     verbose_name = _('profiles')
#