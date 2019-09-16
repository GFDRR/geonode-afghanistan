#!/usr/bin/env bash

. /home/geosolutions/venv/bin/activate

pushd $(dirname $0)

. /home/geosolutions/venv/afg/geonode.env; /home/geosolutions/venv/bin/python /home/geosolutions/venv/afg/manage.py $@

exit 0
