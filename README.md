### PalveluViuhka

Installation
------------

### Prepare and activate virtualenv

- Windows
```shell
python -m venv env
call env/scripts/activate
```

- Linux
```shell
python3 -m venv env
source venv/bin/activate
```


### Install required packages

Install all packages required for development with pip command:

    pip install -r requirements.txt


### Create the database
(also works with MYSQL)

- Linux

```shell
sudo -u postgres psql -c "create role employment with encrypted password 'secure-password';"
sudo -u postgres psql -c "create database employment_flask"
```

- Windows
```shell
psql -U postgres -c "create role employment with encrypted password 'secure-password';"
psql -U postgres -c "create database employment_flask"
```

### Build Employment Search static resources(Optional)

Make sure you have nodejs installed.

- Linux

```shell
chmod +x ./build-resources.sh
./build-resources.sh
```

- Windows
```shell
start build-resources.bat
```

### Dev environment configuration

Create a file `employment/.env` to configure the dev environment e.g.:

```
SQLALCHEMY_TRACK_MODIFICATIONS=1
SECRET_KEY=28419842198412894
SQL_USERNAME=employment
SQL_PASSWORD=
SQL_DATABASE=employment_flask
SQL_PORT=5432
DEBUG=0
```
### Run Django migrations and import data

```shell
python manage.py migrate
python manage.py createsuperuser
```
