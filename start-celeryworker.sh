#!/bin/bash

set -o errexit
set -o nounset

celery -A smart_energy worker -l INFO
