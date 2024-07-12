#!/bin/bash

# Ensure that Python and pip are installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Installing Python3..."
    apt-get update
    apt-get install -y python3 python3-pip
fi

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
