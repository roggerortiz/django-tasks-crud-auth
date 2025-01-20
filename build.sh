#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install requirements
python3 -m pip install -r requirements.txt

# Convert static asset files
python3 manage.py collectstatic --noinput

# Apply any outstanding database migrations
python3 manage.py makemigrations
python3 manage.py migrate
