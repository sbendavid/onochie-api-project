#!/bin/bash

# Install Python and pip
apt-get update
apt-get install -y python3 python3-pip python3-venv

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Deactivate virtual environment
deactivate
