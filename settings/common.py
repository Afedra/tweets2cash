# -*- coding: utf-8 -*-

import sys, os
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

APPEND_SLASH = config('APPEND_SLASH', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS',cast=Csv())

CELERY_ENABLED = config('CELERY_ENABLED', default=False, cast=bool)
CELERY_RESULT_BACKEND = 'django-db'

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.postgres",

    "djmail",
    "django_jinja",
    "django_jinja.contrib._humanize",
    "sr",
    "easy_thumbnails",
    'django_extensions',
    'django_sites',
    'rest_framework',
    'django_celery_results',
    'django_celery_beat',
    'notifications',

    "tweets2cash.base",
    "tweets2cash.auth.apps",
    "tweets2cash.front",
    "tweets2cash.users",
    
]


#sNOTIFICATIONS_USE_JSONFIELD=True
MIDDLEWARE = [
    "tweets2cash.base.middleware.cors.CoorsMiddleware",

    'django.middleware.security.SecurityMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tweets2cash.urls'

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "match_extension": ".jinja",
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        }
    },
]

WSGI_APPLICATION = 'tweets2cash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "tweets2cash",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": os.path.join(BASE_DIR, '.cache')
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# The absolute url is mandatory because attachments
# urls depends on it. On production should be set
# something like https://media.tweets2cash.com/
# MEDIA_URL = "http://localhost:8000/media/"
# STATIC_URL = "http://localhost:8000/static/"
MEDIA_URL = "/media/"
STATIC_URL = "/static/"

# Static configuration.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = (
   os.path.join(BASE_DIR, "static"),
    # Put strings here, like "/home/tweets2cash/static" or "C:/www/django/static".
    # Don't forget to use absolute paths, not relative paths.
)

USE_X_FORWARDED_HOST = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

ATOMIC_REQUESTS = True

LOGIN_URL = "/"

# Languages we provide translations for, out of the box.
LANGUAGES = [
    #("af", "Afrikaans"),  # Afrikaans
    #("ar", "العربية‏"),  # Arabic
    #("ast", "Asturiano"),  # Asturian
    #("az", "Azərbaycan dili"),  # Azerbaijani
    #("bg", "Български"),  # Bulgarian
    #("be", "Беларуская"),  # Belarusian
    #("bn", "বাংলা"),  # Bengali
    #("br", "Bretón"),  # Breton
    #("bs", "Bosanski"),  # Bosnian
    # ("ca", "Català"),  # Catalan
    #("cs", "Čeština"),  # Czech
    #("cy", "Cymraeg"),  # Welsh
    #("da", "Dansk"),  # Danish
    # ("de", "Deutsch"),  # German
    #("el", "Ελληνικά"),  # Greek
    ("en", "English (US)"),  # English
    #("en-au", "English (Australia)"),  # Australian English
    #("en-gb", "English (UK)"),  # British English
    #("eo", "esperanta"),  # Esperanto
    # ("es", "Español"),  # Spanish
    #("es-ar", "Español (Argentina)"),  # Argentinian Spanish
    #("es-mx", "Español (México)"),  # Mexican Spanish
    #("es-ni", "Español (Nicaragua)"),  # Nicaraguan Spanish
    #("es-ve", "Español (Venezuela)"),  # Venezuelan Spanish
    #("et", "Eesti"),  # Estonian
    #("eu", "Euskara"),  # Basque
    #("fa", "فارسی‏"),  # Persian
    # ("fi", "Suomi"),  # Finnish
    # ("fr", "Français"),  # French
    #("fy", "Frysk"),  # Frisian
    #("ga", "Irish"),  # Irish
    #("gl", "Galego"),  # Galician
    #("he", "עברית‏"),  # Hebrew
    #("hi", "हिन्दी"),  # Hindi
    #("hr", "Hrvatski"),  # Croatian
    #("hu", "Magyar"),  # Hungarian
    #("ia", "Interlingua"),  # Interlingua
    #("id", "Bahasa Indonesia"),  # Indonesian
    #("io", "IDO"),  # Ido
    #("is", "Íslenska"),  # Icelandic
    # ("it", "Italiano"),  # Italian
    # ("ja", "日本語"),  # Japanese
    #("ka", "ქართული"),  # Georgian
    #("kk", "Қазақша"),  # Kazakh
    #("km", "ភាសាខ្មែរ"),  # Khmer
    #("kn", "ಕನ್ನಡ"),  # Kannada
    # ("ko", "한국어"),  # Korean
    #("lb", "Lëtzebuergesch"),  # Luxembourgish
    #("lt", "Lietuvių"),  # Lithuanian
    #("lv", "Latviešu"),  # Latvian
    #("mk", "Македонски"),  # Macedonian
    #("ml", "മലയാളം"),  # Malayalam
    #("mn", "Монгол"),  # Mongolian
    #("mr", "मराठी"),  # Marathi
    #("my", "မြန်မာ"),  # Burmese
    # ("nb", "Norsk (bokmål)"),  # Norwegian Bokmal
    #("ne", "नेपाली"),  # Nepali
    # ("nl", "Nederlands"),  # Dutch
    #("nn", "Norsk (nynorsk)"),  # Norwegian Nynorsk
    #("os", "Ирон æвзаг"),  # Ossetic
    #("pa", "ਪੰਜਾਬੀ"),  # Punjabi
    # ("pl", "Polski"),  # Polish
    #("pt", "Português (Portugal)"),  # Portuguese
    # ("pt-br", "Português (Brasil)"),  # Brazilian Portuguese
    #("ro", "Română"),  # Romanian
    # ("ru", "Русский"),  # Russian
    #("sk", "Slovenčina"),  # Slovak
    #("sl", "Slovenščina"),  # Slovenian
    #("sq", "Shqip"),  # Albanian
    #("sr", "Српски"),  # Serbian
    #("sr-latn", "srpski"),  # Serbian Latin
    # ("sv", "Svenska"),  # Swedish
    #("sw", "Kiswahili"),  # Swahili
    #("ta", "தமிழ்"),  # Tamil
    #("te", "తెలుగు"),  # Telugu
    #("th", "ภาษาไทย"),  # Thai
    # ("tr", "Türkçe"),  # Turkish
    #("tt", "татар теле"),  # Tatar
    #("udm", "удмурт кыл"),  # Udmurt
    #("uk", "Українська"),  # Ukrainian
    #("ur", "اردو‏"),  # Urdu
    #("vi", "Tiếng Việt"),  # Vietnamese
    # ("zh-hans", "中文(简体)"),  # Simplified Chinese
    # ("zh-hant", "中文(香港)"),  # Traditional Chinese
]

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = ["he", "ar", "fa", "ur"]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "tweets2cash", "locale"),
)

SITES = {
   "website": {
      "scheme": "https",
      "domain": "localhost.com",
      "name": "website"
   },
}

SITE_ID = "website"

# Session configuration (only used for admin)
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = config('MAX_AGE_CANCEL_ACCOUNT', default=1209600, cast=int) # (2 weeks)

# MAIL OPTIONS
DEFAULT_FROM_EMAIL = "info@tweets2cash.com"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DJMAIL_REAL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DJMAIL_SEND_ASYNC = True
DJMAIL_MAX_RETRY_NUMBER = 3
DJMAIL_TEMPLATE_EXTENSION = "jinja"

# Message System
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Defautl storage
DEFAULT_FILE_STORAGE = "tweets2cash.base.storage.FileSystemStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "formatters": {
        "complete": {
            "format": "%(levelname)s:%(asctime)s:%(module)s %(message)s"
        },
        "simple": {
            "format": "%(levelname)s:%(asctime)s: %(message)s"
        },
        "null": {
            "format": "%(message)s",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        },
    },
    "handlers": {
        "null": {
            "level":"DEBUG",
            "class":"logging.NullHandler",
        },
        "console":{
            "level":"DEBUG",
            "class":"logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django": {
            "handlers":["null"],
            "propagate": True,
            "level":"INFO",
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "tweets2cash": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        }
    }
}

AUTH_USER_MODEL = "users.User"
FORMAT_MODULE_PATH = "tweets2cash.base.formats"

DATE_INPUT_FORMATS = (
    "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%b %d %Y",
    "%b %d, %Y", "%d %b %Y", "%d %b, %Y", "%B %d %Y",
    "%B %d, %Y", "%d %B %Y", "%d %B, %Y"
)

MAX_AGE_AUTH_TOKEN = config('MAX_AGE_AUTH_TOKEN', default=None, cast=int)
MAX_AGE_CANCEL_ACCOUNT = config('MAX_AGE_CANCEL_ACCOUNT', default=2592000, cast=int)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # Mainly used by front
        "tweets2cash.auth.backends.Token",

        # Mainly used for api debug.
        "tweets2cash.auth.backends.Session",
    ),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.CommonThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon-write": None,
        "user-write": None,
        "anon-read": None,
        "user-read": None,
        "login-fail": None,
        "register-success": None,
        "user-detail": None,
        "user-update": None,
    },
    "DEFAULT_THROTTLE_WHITELIST": [],
    "FILTER_BACKEND": "rest_framework.filters.FilterBackend",
    "PAGINATE_BY": 30,
    "PAGINATE_BY_PARAM": "page_size",
    "MAX_PAGINATE_BY": 1000,
    "DATETIME_FORMAT": "%d %B %Y %H:%M"
}

"""
PREDEFINED_COLORS = ["#fce94f", "#edd400", "#c4a000", "#8ae234",
                      "#73d216", "#4e9a06", "#d3d7cf", "#fcaf3e",
                      "#f57900", "#ce5c00", "#729fcf", "#3465a4",
                      "#204a87", "#888a85", "#ad7fa8", "#75507b",
                      "#5c3566", "#ef2929", "#cc0000", "#a40000",
                      "#2e3436",]
"""

# Extra expose header related to tweets2cash APP (see base.middleware.cors=)
APP_EXTRA_EXPOSE_HEADERS = []

PUBLIC_REGISTER_ENABLED = config('PUBLIC_REGISTER_ENABLED', default=True, cast=bool)

# None or [] values in USER_EMAIL_ALLOWED_DOMAINS means allow any domain
USER_EMAIL_ALLOWED_DOMAINS  = config('USER_EMAIL_ALLOWED_DOMAINS', default=None, cast=Csv())

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}


THN_AVATAR_SIZE = 80                # 80x80 pixels
THN_AVATAR_BIG_SIZE = 300           # 300x300 pixels
THN_LOGO_SMALL_SIZE = 80            # 80x80 pixels
THN_LOGO_BIG_SIZE = 300             # 300x300 pixels
THN_TIMELINE_IMAGE_SIZE = 640       # 640x??? pixels
THN_CARD_IMAGE_WIDTH = 300          # 300 pixels
THN_CARD_IMAGE_HEIGHT = 200         # 200 pixels
THN_PREVIEW_IMAGE_WIDTH = 800       # 800 pixels

THN_AVATAR_SMALL = "avatar"
THN_AVATAR_BIG = "big-avatar"
THN_LOGO_SMALL = "logo-small"
THN_LOGO_BIG = "logo-big"
THN_ATTACHMENT_TIMELINE = "timeline-image"
THN_ATTACHMENT_CARD = "card-image"
THN_ATTACHMENT_PREVIEW = "preview-image"

THUMBNAIL_ALIASES = {
    "": {
        THN_AVATAR_SMALL: {"size": (THN_AVATAR_SIZE, THN_AVATAR_SIZE), "crop": True},
        THN_AVATAR_BIG: {"size": (THN_AVATAR_BIG_SIZE, THN_AVATAR_BIG_SIZE), "crop": True},
        THN_LOGO_SMALL: {"size": (THN_LOGO_SMALL_SIZE, THN_LOGO_SMALL_SIZE), "crop": True},
        THN_LOGO_BIG: {"size": (THN_LOGO_BIG_SIZE, THN_LOGO_BIG_SIZE), "crop": True},
        THN_ATTACHMENT_TIMELINE: {"size": (THN_TIMELINE_IMAGE_SIZE, 0), "crop": True},
        THN_ATTACHMENT_CARD: {"size": (THN_CARD_IMAGE_WIDTH, THN_CARD_IMAGE_HEIGHT), "crop": True},
        THN_ATTACHMENT_PREVIEW: {"size": (THN_PREVIEW_IMAGE_WIDTH, 0), "crop": False},
    },
}

# If is True /front/sitemap.xml show a valid sitemap of tweets2cash-front client
FRONT_SITEMAP_ENABLED = config('FRONT_SITEMAP_ENABLED', default=True, cast=bool)
FRONT_SITEMAP_CACHE_TIMEOUT = config('FRONT_SITEMAP_CACHE_TIMEOUT', cast=int)  # In second

from .sr import *

# NOTE: DON'T INSERT MORE SETTINGS AFTER THIS LINE
TEST_RUNNER="django.test.runner.DiscoverRunner"

TWITTER_ACCESS_TOKEN = config('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = config('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_CONSUMER_KEY = config('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET')
# The maximum number of characters in a tweet.
MAX_TWEET_SIZE = config('MAX_TWEET_SIZE', default=140, cast=int)
# The number of worker threads processing tweets.
NUM_THREADS = config('NUM_THREADS', default=100, cast=int)
# The maximum time in seconds that workers wait for a new task on the queue.
QUEUE_TIMEOUT_S = config('QUEUE_TIMEOUT_S', default=1, cast=int)
# The number of retries to attempt when an error occurs.
API_RETRY_COUNT = config('API_RETRY_COUNT', default=60, cast=int)
# The number of seconds to wait between retries.
API_RETRY_DELAY_S = config('API_RETRY_DELAY_S', default=1, cast=int)
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, "settings", config('GOOGLE_APPLICATION_CREDENTIALS'))
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", GOOGLE_APPLICATION_CREDENTIALS)


if "test" in sys.argv:
    print ("\033[1;91mNo django tests.\033[0m")
    print ("Try: \033[1;33mpy.test\033[0m")
    sys.exit(0)
