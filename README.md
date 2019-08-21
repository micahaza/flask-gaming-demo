# Simple iGaming platform

# Setup guide

## Prerequisites
* python3

## Setup virtual environment
* python3 -m virtualenv env
* source ./env/bin/activate

## Install required library
* pip install pip --upgrade
* pip install -r requirements.txt

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

### Request and responses

