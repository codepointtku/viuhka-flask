# PalveluViuhka



**Table of Contents**
---
> * [Requirements](#requirements)
> * [Database](#database)
> * [Installation](#installation)


**Requirements**
---
* Windows
  * [MySQL (8.0+)](https://dev.mysql.com/downloads/mysql/)
    * [Alternatively PostgreSQL (10+)](https://www.postgresql.org/download/windows/)
    * [Universal Database Tool DBeaver](https://dbeaver.io/)
      * [Github](https://github.com/dbeaver/dbeaver)
  * [Python3.7](https://www.python.org/downloads/)

* Linux
  * [MariaDB](aaa)
  * [Python3.7](aaa)

**Database**
---
  * Install [MySQL](https://dev.mysql.com/downloads/mysql/) or [PostgreSQL (10+)](https://www.postgresql.org/download/windows/) and follow GUI instructions
  * Install [Python3.7](https://www.python.org/downloads/) and follow GUI instructions
  * Create user and database
  * Create .env file inside the project folder and add the following:
  ```
  SQLALCHEMY_TRACK_MODIFICATIONS=1
  SECRET_KEY=28419842198412894

  SQL_USERNAME=database_username
  SQL_PASSWORD=database_username_password
  SQL_DATABASE=database_name
  SQL_CHARSET=utf8mb4
  SQL_PORT=database_port

  SESSION_COOKIE_SECURE=True
  SESSION_COOKIE_HTTPONLY=True
  SESSION_COOKIE_SAMESITE=Lax
  ```

  ```
  SQL_DRIVER=mysql+pymysql
  ```
  OR
  ```
  SQL_DRIVER=postgresql+psycopg2
  ```
  Depending on which database you chose to install.

**Installation**
---
(Point the system path to MySQL or PostgreSQL executable)

* Create database via CLI
  * MySQL
    * `mysql -h localhost -u username -p`
    * `CREATE DATABASE database_name;`
    * `quit;`
  * PostgreSQL
    * `psql -U postgres -c 'CREATE DATABASE database_name;'`


* Windows
  * `git clone https://github.com/digipointtku/viuhka-flask.git`
  * `cd viuhka-flask`
  * `python -m venv env`
  * `call env/scripts/activate`
  * `pip install -r requirements.txt`
  * `python main.py --create`
  * `python main.py --import`
  * `python main.py`

* Linux
  * `$ git clone https://github.com/digipointtku/viuhka-flask.git`
  * `$ cd viuhka-flask`
  * `$ python3 -m venv env`
  * `$ source env/bin/activate`
  * `$ pip install -r requirements.txt`
  * `$ python main.py --create`
  * `$ python main.py --import`
  * `$ python main.py`
  