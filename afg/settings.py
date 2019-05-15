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
import os
from geonode.local_settings import *
#
# General Django development settings
#

DEBUG = False

SITENAME = 'afg'

ALLOWED_HOSTS = ['198.50.229.90', 'localhost', '127.0.0.1', 'disasterrisk-af-dev.geo-solutions.it', 'disasterrisk.af.geonode.org', 'disasterrisk.af', 'www.disasterrisk.af']

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "afg.wsgi.application"


# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass

SITEURL = "http://disasterrisk.af/"

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
    'geonode.contrib.risks',
)

INSTALLED_APPS = INSTALLED_APPS + GEONODE_CONTRIB_APPS + ('afg',)

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))

#LAYER_PREVIEW_LIBRARY = 'leaflet'
ACCOUNT_OPEN_SIGNUP = False

# use when geonode.contrib.risks is in installed apps.
RISKS = {'DEFAULT_LOCATION': 'AF',
         'PDF_GENERATOR': {'NAME': 'weasyprint_api',
                           #'NAME': 'wkhtml2pdf',
                           'BIN': '/usr/bin/xvfb-run /usr/bin/wkhtmltopdf',
                           'ARGS': []}}

# add following lines to your local settings to enable monitoring
MONITORING_ENABLED = True

if MONITORING_ENABLED:
    if 'geonode.contrib.monitoring' not in INSTALLED_APPS:
        INSTALLED_APPS += ('geonode.contrib.monitoring',)
        if 'geonode.contrib.monitoring.middleware.MonitoringMiddleware' not in MIDDLEWARE_CLASSES:
            MIDDLEWARE_CLASSES += ('geonode.contrib.monitoring.middleware.MonitoringMiddleware',)
        MONITORING_CONFIG = None
        MONITORING_HOST_NAME = os.getenv("MONITORING_HOST_NAME", 'disasterrisk.af')
        MONITORING_SERVICE_NAME = 'geonode'
