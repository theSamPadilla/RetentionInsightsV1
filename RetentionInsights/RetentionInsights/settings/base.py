"""
Base settings for RetentionInsights project.
"""

from pathlib import Path
import os
import environ #type: ignore

# Setting up Environment Variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'settings' / 'this dir'.
# Note that this maps to one parent above than default because this is inside settings dir
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Rewards Verification Token
REWARDS_VERIFY_TOKEN = env('REWARDS_VERIFY_TOKEN')

# Application definition
INSTALLED_APPS = [
    'surveys.apps.SurveysConfig',
    'rewards.apps.RewardsConfig',
    'confirmation.apps.ConfirmationConfig',
    'feedback.apps.FeedbackConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RetentionInsights.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'RetentionInsights.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Email Settings 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_FILE_PATH = '/home/sam/RetentionInsightsV1/logs/email/'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

EMAIL_HOST_USER = 'padilla.samuelk@gmail.com'

EMAIL_PORT = 587

EMAIL_USE_LOCALTIME = True

EMAIL_USE_TLS = True
