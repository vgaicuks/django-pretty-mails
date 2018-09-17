class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(
            settings,
            'PRETTY_SETTING_GETTER',
            lambda name, dflt: getattr(settings, name, dflt)
        )
        return getter(self.prefix + name, dflt)

    @property
    def MAIL_TYPES(self):
        return self._setting('MAIL_TYPES', {})


# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys  # noqa


app_settings = AppSettings('PRETTY_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
