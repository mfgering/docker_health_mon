HOST = ''
CONTAINER = ''
SMTP_SERVER = ''
SMTP_USER = ''
SMTP_PASSWORD = ''
RECIPIENTS = ''
EMAIL_FROM = ''

try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass
