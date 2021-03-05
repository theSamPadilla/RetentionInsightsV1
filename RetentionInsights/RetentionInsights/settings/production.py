"""
Production settings for RetentionInsights project.

Extended from base.py

"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Only allow connections on (www).retentioninsights.io
ALLOWED_HOSTS = [
    'retentioninsights.io',
    'www.retentioninsights.io', 
]

# Database - SQLite for MVP - eventually switch to Postergre
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files - Should be served by NGINX
STATIC_URL = '/static/'
#-------------------------------------------
STATIC_ROOT = '/home/sam/RetentionInsightsV1/static/'
#-------------------------------------------
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# User-generated Media files (jpg, png, vids) ?

# HTTPS settings - Turned off for MVP since not managing authentication
#CSRF_COOKIE_SECURE = True
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True


