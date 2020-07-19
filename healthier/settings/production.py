import os

from . import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# settings for sentry app monitoring.
sentry_sdk.init(
    dsn="https://8a46c6da63b64b3cbc68ae59ede4f046@o406231.ingest.sentry.io/5289045",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data
    send_default_pii=True,
)

SECRET_KEY = os.environ.get("SECRET_KEY")

# settings for email sending : smtp server...
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "pgirmes@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DEBUG = False

ALLOWED_HOSTS = [
    "34.78.192.11",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "purbeurre",
        "HOST": "",
        "PORT": "5432",
        "USER": "paulgirmes",
        "PASSWORD": "Loupi312482..",
    }
}
