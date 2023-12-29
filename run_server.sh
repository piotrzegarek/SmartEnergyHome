#!/bin/bash

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django app
python manage.py runserver 0.0.0.0:8000
