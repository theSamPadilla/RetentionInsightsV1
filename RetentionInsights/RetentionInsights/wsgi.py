"""
WSGI config for RetentionInsights project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Developmet Settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RetentionInsights.settings.development')

# Production Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RetentionInsights.settings.production')

application = get_wsgi_application()
