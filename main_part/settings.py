from pathlib import Path
import os, dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# BASIC SETTINGS
# -------------------------

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")

DEBUG = os.environ.get("DEBUG", "").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# -------------------------
# INSTALLED APPS
# -------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sub_part",
]

ROOT_URLCONF = "main_part.urls"


# -------------------------
# MIDDLEWARE
# -------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------
# TEMPLATES
# -------------------------

TEMPLATES = [
    {
        "BACKEND":"django.template.backends.django.DjangoTemplates",
        "DIRS":[BASE_DIR / "templates"],
        "APP_DIRS":True,
        "OPTIONS":{
            "context_processors":[
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# -------------------------
# STATIC FILES
# -------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------
# DATABASE CONFIG (SAFE)
# -------------------------

raw_db_url = os.environ.get("DATABASE_URL")

def is_valid_database_url(url):
    """Return True only if DATABASE_URL looks like a real URL."""
    if not url:
        return False
    url = url.strip()
    if url in ["", "None", "null", "NULL"]:
        return False
    valid_prefixes = ["postgres://", "postgresql://", "mysql://", "mysql2://"]
    return any(url.lower().startswith(prefix) for prefix in valid_prefixes)

if is_valid_database_url(raw_db_url):
    # PRODUCTION / RAILWAY / POSTGRES
   DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

else:
    # LOCAL DEVELOPMENT — SQLITE
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ["*", ".railway.app"]

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }

# -------------------------
# EMAIL
# -------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT","587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS","true").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# -------------------------
# AUTH REDIRECTS
# -------------------------

LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "landing"
