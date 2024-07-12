# echo "BUILD START"

# # create a virtual environment named 'venv' if it doesn't already exist
# python3.12 -m venv venv

# # activate the virtual environment
# source venv/bin/activate

# # build_files.sh
# python3.12 -m pip install -r requirements.txt

# # make migrations

# python3.12 manage.py collectstatic


# # collect static files using the Python interpreter from venv
# python manage.py collectstatic --noinput

# echo "BUILD END"

# # [optional] Start the application here 
# # python manage.py runserver

#!/bin/bash

# Install pip if not already installed
if ! command -v pip &> /dev/null
then
    echo "pip not found, installing pip"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py --user
fi

# Install dependencies
pip install -r requirements.txt

python3.9 manage.py migrate 