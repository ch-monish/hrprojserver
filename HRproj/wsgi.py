"""
WSGI config for HRproj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'HRproj.settings'
# sys.path.append('C:\\Users\\sbatchu\\AppData\\Roaming\\Python\\Python310\\site-packages')
# sys.path.append('C:\\Users\\sbatchu\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages')


from django.core.wsgi import get_wsgi_application


# os.environ.setdefault("DJANGO_SETTINGS_MODULE","HRproj.settings")



application = get_wsgi_application()
