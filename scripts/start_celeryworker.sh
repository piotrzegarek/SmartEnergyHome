#!/bin/bash

set -o errexit
set -o nounset

celery -A app.config worker -l INFO
