import os

import dj_database_url


def _env_get_required(setting_name):
    """Get the value of an environment variable and assert that it is set."""
    setting = os.environ.get(setting_name)
    assert setting not in {None, ""}, "{0} must be defined as an environment variable.".format(setting_name)
    return setting


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
IN_DEV = ENVIRONMENT in ["development", "ci"]
IN_STAGING = ENVIRONMENT == "staging"
IN_PROD = ENVIRONMENT == "production"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _env_get_required("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _env_get_required("DEBUG") == "True"

if IN_DEV:
    SERVER_EMAIL = "RS Fullstack Development <noreply-dev@server.com>"
elif IN_STAGING:
    SERVER_EMAIL = "RS Fullstack Staging <noreply-staging@server.com>"
else:
    SERVER_EMAIL = "RS Fullstack <noreply@server.com>"

DEFAULT_FROM_EMAIL = SERVER_EMAIL

# Email address of the staff who should receive certain emails
STAFF_EMAIL = os.environ.get("STAFF_EMAIL", "no-reply@revsetter.com")

#
# Domain Configuration
#
CURRENT_DOMAIN = _env_get_required("CURRENT_DOMAIN")
CURRENT_PORT = os.environ.get("CURRENT_PORT")
ALLOWED_HOSTS = []
ALLOWED_HOSTS += _env_get_required("ALLOWED_HOSTS").split(",")
if CURRENT_DOMAIN not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(CURRENT_DOMAIN)

# Application definition

INSTALLED_APPS = [
    # Local
    "server.common",
    "server.core",
    "server.products",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party
    "corsheaders",
    "django_nose",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

OLD_PASSWORD_FIELD_ENABLED = True
LOGIN_URL = "rest_framework:login"
LOGOUT_URL = "rest_framework:logout"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [
            os.path.join(BASE_DIR, "./client/dist/"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "server.wsgi.application"

# Database
"""There are two ways to specify the database connection

1. DATABASE_URL - we use dj_database_url to interpret Heroku's DATABASE_URL env variable.
2. Specify DB_NAME, DB_USER, DB_PASS, and DB_HOST Directly in the env file.
"""
# Update database configuration with dj_database_url
database_con_url = dj_database_url.config(conn_max_age=500)
if bool(database_con_url):
    DATABASES = {"default": database_con_url}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": _env_get_required("DB_NAME"),
            "USER": _env_get_required("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASS", ""),
            "HOST": _env_get_required("DB_HOST"),
            "CONN_MAX_AGE": 600,
        },
    }
#
# User Configuration and Password Validation
#
AUTH_USER_MODEL = "core.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    }
]

#
# Internationalization & Localization Settings
#
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

#
# Django Rest Framework Configuration
#
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "server.core.pagination.PageNumberPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "ALLOWED_VERSIONS": [
        "1.0",
    ],
    "DEFAULT_VERSION": "1.0",
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
}
if DEBUG or IN_DEV:  # for testing
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append("rest_framework.renderers.BrowsableAPIRenderer")
#
# Static files (CSS, JavaScript, Images)
#
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "./client/dist/static"),
]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Anymail
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]  # noqa F405
if not IN_DEV:

    #
    # Custom SMTP settings
    #
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    ANYMAIL = {}
    EMAIL_HOST = _env_get_required("SMTP_HOST")
    EMAIL_PORT = os.environ.get("SMTP_PORT", 587)
    EMAIL_HOST_USER = _env_get_required("SMTP_USER")
    EMAIL_HOST_PASSWORD = _env_get_required("SMTP_PASSWORD")
    EMAIL_ALLOWED_DOMAINS = _env_get_required("SMTP_VALID_TESTING_DOMAINS")
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# STORAGES
# ----------------------------------------------------------------------------

PRIVATE_MEDIAFILES_LOCATION = ""

#
# STATIC
# ------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # i.e. 2.5 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # i.e. 10 MB

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("revsetter", "support@revsetter.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
#
# HTTPS Everywhere outside the dev environment
#
if not IN_DEV:
    # SECURE_SSL_REDIRECT = True
    # SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    MIDDLEWARE += ["django.middleware.security.SecurityMiddleware"]
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_HSTS_SECONDS = 60
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'

    ADMINS += [
        ('Gergely Karoly-Bela', 'karoly.gergely@spiderlinked.com'),
    ]
#
# Custom logging configuration
#
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "WARNING",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "mail_admins"], "level": "INFO"},
        # The logger name matters -- it MUST match the name of the app
        "server": {"handlers": ["console", "mail_admins"], "level": "DEBUG", "propagate": True},
        "server.request": {"handlers": [], "level": "INFO", "propagate": True},
        "server.tasks": {"handlers": [], "level": "INFO", "propagate": True},
    },
}

# Popular testing framework that allows logging to stdout while running unit tests
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# FILE STORAGE
MEDIA_URL = '/'
MEDIAFILES_LOCATION = 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

if IN_PROD or IN_STAGING:
    # S3 storage
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_QUERYSTRING_AUTH = False
    AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
    MEDIA_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN,
                                        MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'server.utils.custom_storages.MediaStorage'
    AWS_S3_SIGNATURE_VERSION = 's3v4'

# API DOCS
INSTALLED_APPS += ['drf_spectacular', ]
REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'
SPECTACULAR_SETTINGS = {
    'TITLE': 'RS FULL STACK API',
    'DESCRIPTION': 'A comprehensive product gallery application enabling '
                   'users to register, log in, and manage '
                   '(add/update/delete) products. Each product should '
                   'include attributes such as name, price, description, '
                   'and images.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
}

# Locales
LANGUAGES = [('en', 'English'), ]
LOCALE_PATHS = os.path.join(os.path.dirname(__file__), "locale"),

# CORS
if IN_PROD or IN_STAGING:
    CORS_ORIGIN_WHITELIST = *os.environ.get('CORS_WHITELIST', '').split(', '),
    CORS_ORIGIN_REGEX_WHITELIST = [
        r'%s' % regex for regex
        in os.environ.get('CORS_WHITELIST_REGEX', '').split(', ')
    ]
else:
    CORS_ALLOW_ALL_ORIGINS = True
