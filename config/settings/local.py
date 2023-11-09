"""Project local settings."""
from config.settings.base import *  # noqa: F403, F401
from config.settings.utils import get_bool_env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env("DEBUG")

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"