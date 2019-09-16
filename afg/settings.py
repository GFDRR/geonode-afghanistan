# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import ast
import os
from urlparse import urlparse, urlunparse
# Load more settings from a file called local_settings.py if it exists
try:
    from geonode.local_settings import *
except ImportError:
    from geonode.settings import *

#
# General Django development settings
#

DEBUG = False

SITENAME = 'afg'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'disasterrisk-af-dev.geo-solutions.it', 'www.disasterrisk-af-dev.geo-solutions.it']

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "afg.wsgi.application"

# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass

SITEURL = "https://disasterrisk-af-dev.geo-solutions.it/"

# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(LOCAL_ROOT, "static"),
)

# Location of url mappings
ROOT_URLCONF = 'afg.urls'

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

GEONODE_CONTRIB_APPS = (
    'geonode_risks',
)

INSTALLED_APPS = INSTALLED_APPS + GEONODE_CONTRIB_APPS + ('afg',)

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))

# Login and logout urls override
LOGIN_URL = os.getenv('LOGIN_URL', '{}account/login/'.format(SITEURL))
LOGOUT_URL = os.getenv('LOGOUT_URL', '{}account/logout/'.format(SITEURL))

ACCOUNT_LOGIN_REDIRECT_URL = os.getenv('LOGIN_REDIRECT_URL', SITEURL)
ACCOUNT_LOGOUT_REDIRECT_URL =  os.getenv('LOGOUT_REDIRECT_URL', SITEURL)
ACCOUNT_OPEN_SIGNUP = False

# use when geonode.contrib.risks is in installed apps.
RISKS = {'DEFAULT_LOCATION': 'AF',
         'PDF_GENERATOR': {'NAME': 'weasyprint_api',
                           #'NAME': 'wkhtml2pdf',
                           'BIN': '/usr/bin/xvfb-run /usr/bin/wkhtmltopdf',
                           'ARGS': []}}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode_risks": {
            "handlers": ["console"], "level": "DEBUG", },
        "geonode.qgis_server": {
            "handlers": ["console"], "level": "ERROR", },
        "geoserver-restconfig.catalog": {
            "handlers": ["console"], "level": "ERROR", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "ERROR", },
        "celery": {
            "handlers": ["console"], "level": "ERROR", },
    },
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
