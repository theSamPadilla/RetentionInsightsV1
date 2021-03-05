"""
Dev settings for RetentionInsights project.

Extended from base

"""

from .base import *


# Debug is always True in Development
DEBUG = True

# Allowed hosts includes all
ALLOWED_HOSTS = [
    'retentioninsights.io',
    'www.retentioninsights.io', 
    'dev.retentioninsights.io', 
    'test.retentioninsights.io', 
    '35.208.177.121', 
    '127.0.0.1',
]

# Database - SQLite by default for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images) - Served locally
STATIC_URL = '/static/'
#-------------------------------------------
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
#-------------------------------------------
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

