from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Toutes les données sensibles sont ailleurs
env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")
# Gestion des emails
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DATABASES = {
        'default': env.db(
            'DATABASE_URL',
            engine='django.db.backends.postgresql'
            ),
    }
# Envoi d'e-mail
EMAIL_HOST = env("EMAIL_HOST")  # ex: smtp-1.alwaysdata.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env("HOST_USER")
EMAIL_HOST_PASSWORD = env("HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "kwargs SRL <info@kwargs.be>"
EMAIL_SUBJECT_PREFIX = "[kwargs notification]"

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    "crispy_bootstrap5",
    'crispy_forms',
    "debug_toolbar",
    "taggit",
    "ressource", # pour pas foutre la merde, "ressource" doit être placé avant "allauth"
    # Traduction
    "rosetta",
    # All-auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'page',
    "workload",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'celen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'gabarits',
            BASE_DIR / 'gabarits/registration',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'celen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True

LANGUAGES = (
    ('fr', _('Français')),
    ('en', _('Anglais')),
    ('es', _('Espagnol')),
    ('ar', _('Arabe')),
    ('nl', _('Néerlandais')),
)

ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = "fr"
USE_THOUSAND_SEPARATOR = True
ROSETTA_EXCLUDED_APPLICATIONS = (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
)
LOCALE_PATHS = [BASE_DIR / 'locale', BASE_DIR / 'gabarits/registration/locale',]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_ROOT = BASE_DIR/'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR/'static',
]
MEDIA_ROOT = BASE_DIR/'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
]

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

# Django-AllAuth
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_LOGIN_METHODS = {"username","email"}
ACCOUNT_SIGNUP_FIELDS = ['username', 'email*', 'password1*', 'password2*']
LOGIN_REDIRECT_URL = 'ressource:profile'
SOCIALACCOUNT_AUTO_SIGNUP = True

# Vérification de l'adresse e-mail
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # 'optional' ou 'none' si tu veux désactiver
ACCOUNT_CONFIRM_EMAIL_ON_GET = True       # Activation immédiate quand on clique (optionnel)

# Connexion automatique après activation
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True


ACCOUNT_ADAPTER = "ressource.adapters.KwargsAccountAdapter"

#ACCOUNT_ADAPTER = 'ressource.adapters.kwargsAccountAdapter'
#SOCIALACCOUNT_ADAPTER = 'ressource.adapters.kwargsSocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_SECRET_KEY'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'APP': {
            'client_id': env('GITHUB_CLIENT_ID'),
            'secret': env('GITHUB_SECRET_KEY'),
            'key': ''
        }
    },
}