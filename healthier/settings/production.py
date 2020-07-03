import os

from . import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
            dsn="https://8a46c6da63b64b3cbc68ae59ede4f046@o406231.ingest.sentry.io/5289045",
            integrations=[DjangoIntegration()],
            # If you wish to associate users to errors (assuming you are using
            # django.contrib.auth) you may enable sending PII data
            send_default_pii=True
            )

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False
ALLOWED_HOSTS = [
        '165.22.87.54',
        ]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "purbeurre",
        "HOST": "",
        "PORT": "5432",
        "USER": "paul",
        "PASSWORD": "Loupi312482.",
        }
}