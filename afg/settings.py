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

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'disasterrisk.af', 'www.disasterrisk.af']

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "afg.wsgi.application"

# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass

SITEURL = "https://disasterrisk.af/"

CLIENT_RESULTS_LIMIT = 4
AVATAR_GRAVATAR_SSL = True

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
            'level': 'DEBUG',
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
            "handlers": ["console"], "level": "INFO", },
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
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"], "level": "DEBUG", },
        "geonode_logstash.logstash": {
            "handlers": ["console"], "level": "DEBUG", },
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


# Settings for MONITORING plugin
MONITORING_ENABLED = ast.literal_eval(os.environ.get('MONITORING_ENABLED', 'True'))

MONITORING_CONFIG = os.getenv("MONITORING_CONFIG", None)
MONITORING_HOST_NAME = os.getenv("MONITORING_HOST_NAME", 'geonode')
MONITORING_SERVICE_NAME = os.getenv("MONITORING_SERVICE_NAME", 'local-geonode')

# how long monitoring data should be stored
MONITORING_DATA_TTL = timedelta(days=int(os.getenv("MONITORING_DATA_TTL", 365)))

# this will disable csrf check for notification config views,
# use with caution - for dev purpose only
MONITORING_DISABLE_CSRF = ast.literal_eval(os.environ.get('MONITORING_DISABLE_CSRF', 'False'))

if MONITORING_ENABLED:
    if 'geonode.monitoring' not in INSTALLED_APPS:
        INSTALLED_APPS += ('geonode.monitoring',)
    if 'geonode.monitoring.middleware.MonitoringMiddleware' not in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES += \
            ('geonode.monitoring.middleware.MonitoringMiddleware',)

    # skip certain paths to not to mud stats too much
    MONITORING_SKIP_PATHS = ('/api/o/',
                             '/monitoring/',
                             '/admin',
                             '/jsi18n',
                             STATIC_URL,
                             MEDIA_URL,
                             re.compile('^/[a-z]{2}/admin/'),
                             )

    # configure aggregation of past data to control data resolution
    # list of data age, aggregation, in reverse order
    # for current data, 1 minute resolution
    # for data older than 1 day, 1-hour resolution
    # for data older than 2 weeks, 1 day resolution
    MONITORING_DATA_AGGREGATION = (
        (timedelta(seconds=0), timedelta(minutes=1),),
        (timedelta(days=1), timedelta(minutes=60),),
        (timedelta(days=14), timedelta(days=1),),
    )

    CELERY_BEAT_SCHEDULE['collect_metrics'] = {
        'task': 'geonode.monitoring.tasks.collect_metrics',
        'schedule': 600.0,
    }

USER_ANALYTICS_ENABLED = ast.literal_eval(os.getenv('USER_ANALYTICS_ENABLED', 'True'))
USER_ANALYTICS_GZIP = ast.literal_eval(os.getenv('USER_ANALYTICS_GZIP', 'True'))

GEOIP_PATH = os.getenv('GEOIP_PATH', os.path.join(PROJECT_ROOT, 'GeoIPCities.dat'))
# -- END Settings for MONITORING plugin

if USER_ANALYTICS_ENABLED and 'geonode_logstash' not in INSTALLED_APPS:
    INSTALLED_APPS += ('geonode_logstash',)

    CELERY_BEAT_SCHEDULE['dispatch_metrics'] = {
        'task': 'geonode_logstash.tasks.dispatch_metrics',
        'schedule': 3600.0,
    }

