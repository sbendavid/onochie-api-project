echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.12 -m venv venv

# activate the virtual environment
source venv/bin/activate

# build_files.sh
python3.12 -m pip install -r requirements.txt

# make migrations
python3.12 manage.py migrate 
python3.12 manage.py collectstatic


# collect static files using the Python interpreter from venv
python manage.py collectstatic --noinput

echo "BUILD END"

# [optional] Start the application here 
# python manage.py runserver