#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python job/manage.py migrate
python job/manage.py collectstatic --no-input