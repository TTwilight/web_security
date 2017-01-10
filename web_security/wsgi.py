"""
WSGI config for web_security project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from os.path import join,dirname,abspath
from django.core.wsgi import get_wsgi_application
import sys

PROJECT_DIR = dirname(dirname(abspath(__file__)))  # 3

sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_security.settings")

application = get_wsgi_application()
