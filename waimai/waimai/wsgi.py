"""
WSGI config for waimai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waimai.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waimai.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waimai.settings.production')

application = get_wsgi_application()
