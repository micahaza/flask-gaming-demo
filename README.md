# Simple iGaming platform

## Assumptions
We assume that bonus money balance will be always divisible with the bet amount so we won't have bonus money wallets holding less than a bet amount. We consider wallets having less than a bet or empty as depleted.

# Setup guide

## Prerequisites
* python3, mysql server

## Setup virtual environment
* python3 -m virtualenv env
* source ./env/bin/activate

## Install required library
* pip install pip --upgrade
* pip install -r requirements.txt

## Configuring the app
You have to create a folder called instance in the project root. Create two files, development.cfg, testing.cfg

Example content of these files (development.cfg):
```
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/flask_gaming_dev'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '2s-odAVOokF7bOgzFQqkPD0s6oiz7IAlnnA3I4ogwZUarxbtJDqKin3alZxRaL1U'

LOGIN_BONUS = 100
DEPOSIT_BONUS = 20
WAGERING_REQUIREMENT = 20
```

## Database install && migrate
* mysql> CREATE DATABASE flask_gaming_dev;
* mysql> CREATE DATABASE flask_gaming_test;
* export FLASK_APP=run.py
* flask db init
* flask db migrate
* flask db upgrade

## Run tests
* export FLASK_ENV=development
* export FLASK_APP=run.py
* py.test -v

### Run the app
* ./start.sh