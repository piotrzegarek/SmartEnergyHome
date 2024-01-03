#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A smart_energy beat -l INFO
