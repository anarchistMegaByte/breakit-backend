# breakit-backend

## Steps of installation

### Clone the github repository from [here](https://github.com/anarchistMegaByte/breakit-backend.git)
>>> git clone https://github.com/anarchistMegaByte/breakit-backend.git


### Activating python3 virtual env.
```
pip install virtualenv
virtualenv -p python3 env-name
source env-name/bin/activate (basically path to activate script of env)
```

### Installing required libraries.

>>> Navigate to project folder and activate the environment before executing this command.

```
pip install -r requirements.txt
```

### Installing supervisor.

>>> This is optional only if you have to schedule tasks. (Support for ubuntu systems. Windows system needs more [configurations](https://pypi.org/project/supervisor-win/)).

```
sudo apt-get install supervisor
```

### Installing postgresql and create a sample Database locally.

>>> If on Ubuntu follow steps given in [link1](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04) and [link2](https://medium.com/chingu/how-i-setup-postgresql-with-django-1-11-in-ubuntu-17-04-lts-85e51669e153
).

```
General steps are as follows for ubuntu system:

sudo apt-get install postgresql-12

Steps to create a Database:


sudo -u postgres psql
postgres=# CREATE DATABASE sampledb; 
CREATE DATABASE
postgres=# CREATE USER sampleUser WITH PASSWORD 'password'; 
CREATE ROLE
postgres=# ALTER ROLE sampleUser SET client_encoding TO 'utf8'; 
ALTER ROLE
postgres=# ALTER ROLE sampleUser SET default_transaction_isolation TO 'read committed'; 
ALTER ROLE
postgres=# ALTER ROLE sampleUser SET timezone TO 'UTC'; 
ALTER ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE sampledb TO sampleUser; 
GRANT
postgres=# \q


Postgresg USer : postgres
Database Name : sampledb
Database User : sampleUser
Database Password : password

```


### Perform Database Migrations

```
python manage.py makemigratios
python manage.py migrate
```


### Install Redis Server
```
sudo apt install redis-server
```


### Run server locally.

```
python manage.py runserver 0.0.0.0:8000
```

### Get your local IP [address](https://tecadmin.net/check-ip-address-ubuntu-18-04-desktop/)

Now you can use this endpoint for the front end applications.


