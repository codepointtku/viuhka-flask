PalveluViuhka
Installation
Prepare and activate virtualenv

* Windows

python -m venv env
call env/scripts/activate

* Linux

python3 -m venv env
source venv/bin/activate

Install required packages

Install all packages required for development with pip command:

pip install -r requirements.txt

Create the database

* Linux

sudo -u postgres psql -c "create role employment with encrypted password 'secure-password';"
sudo -u postgres psql -c "create database employment_flask"

* Windows

psql -U postgres -c "create role employment with encrypted password 'secure-password';"
psql -U postgres -c "create database employment_flask"

Dev environment configuration

Create a file employment/.env to configure the dev environment e.g.:

SQLALCHEMY_TRACK_MODIFICATIONS=1
SECRET_KEY=
SQL_USERNAME=employment
SQL_PASSWORD=
SQL_DATABASE=employment_flask
SQL_PORT=
DEBUG=0

Run Django migrations and import data

python manage.py migrate
python manage.py createsuperuser
