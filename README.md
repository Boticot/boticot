<img alt="Boticot" src="https://github.com/Boticot/boticot/blob/master/admin/src/assets/boticot.png"><br>

# Bot Interface and Conversational Toolkit

[![Release Date](https://img.shields.io/github/v/release/boticot/boticot)](https://github.com/boticot/boticot/releases)
[![Release Date](https://img.shields.io/github/release-date/boticot/boticot)](https://github.com/boticot/boticot/releases)

[![Contributors](https://img.shields.io/github/contributors-anon/boticot/boticot)](https://github.com/boticot/boticot/graphs/contributors)
[![License](https://img.shields.io/github/license/boticot/boticot)](https://github.com/boticot/boticot/blob/master/LICENSE)

Boticot is an open source natural language understanding toolkit. You can use it to create virtual assistant, chatbot and NLU agents.
Boticot helps managing conversations contexts and multiple agents at the same time.
It also improves your user experience thanks to analytics and tracking tools provided with Boticot Admin.

<img alt="Boticot" src="https://github.com/Boticot/boticot/blob/master/admin/src/assets/boticot-tutorial.gif"><br>

##### Features provided by Boticot:
* Manage training data and create intents and entities using user interface
* Track in real time users inputs and improve you agent model based on real user data
* Manage automatic responses for intents: texts, rich texts, suggestions, links and images
* Manage synonyms
* Supervise agent performance with provided analytics
* Manage multiple agents
* Manage users with roles
* Export agents and models

Boticot is based on rasa NLU (version 1.5.3).

## Run all services using Docker-compose

If you simply want to use the toolkit, you can run everything using ``docker-compose up -f docker-compose-boticot-mongo.yml`` (or use ``docker-compose up -f docker-compose-boticot.yml`` if you already have a MongoDB database running). 
If you want to run each service individually, read the following QuickStart guides.

## Boticot API QuickStart

#### Project setup

Recommended Python version: **3.6.8**

You should be in /api folder and follow the next steps:

#### Install dependencies
```
pip install rasa==1.5.3
pip install Tensorflow-datasets==1.3.0
pip install Flask-PyMongo==2.3.0
pip install flask==1.1.2
pip install flask_cors==3.0.8
pip install flask-compress==1.5.0
pip install flask_jwt_extended==3.24.1
pip install isodate==0.6.0
pip install bcrypt==3.2.0
pip install pytest==6.2.5
pip install pytest-mock==3.6.1
pip install gym==0.15.3
```

#### Set up authentication configuration
Before running the project for the first time and for a security purpose, you should replace the default values of environment variables inside api:
* JWT_SECRET_KEY
* ADMIN_LOGIN
* ADMIN_PWD
The ADMIN_LOGIN and ADMIN_PWD will be used for authentication inside Boticot Admin

#### Run API
```
flask run --port 8010
```

To launch tests, simply run ``pytest``. You can select a specific test file to run by appending it to the command.

#### Local Environment variables
To use your local environment variables for development, you need to create a new file .env in api folder and override default exisiting value in .flaskenv file.
Your local .env file will be ignored by git.


## Boticot Admin QuickStart

Recommended NodeJS version: **16.18**

You should be in /admin folder and follow the next steps:

#### Install dependencies
```
yarn install
```

#### Run with hot-reload for development
```
yarn serve
```

## Boticot Trainer QuickStart

#### Project setup

Recommended Python version: **3.6.8**

You should be in /trainer folder and follow the next steps:

#### Install dependencies
```
pip install rasa==1.5.3
pip install Tensorflow-datasets==1.3.0
pip install Flask-PyMongo==2.3.0
pip install flask==1.1.2
pip install flask_cors==3.0.8
pip install flask-compress==1.5.0
pip install isodate==0.6.0
```

#### Run Trainer
```
flask run --port 8011
```

### Local Environment variables
To use your local environment variables for development, you need to create a new file .env in trainer folder and override default exisiting value in .flaskenv file.
Your local .env file will be ignored by git.

## Run database

You must either use a local database or run ``docker-compose up -f docker-compose-boticot-mongo.yml`` in order to get a MongoDB instance running.

Make sure the login & password are the same for the database and the API connection string.

Note: You can select a volume path for the mongo container in ``docker-compose-boticot-mongo.yml`` in order to keep the data when the database Docker goes down.

## Default port mapping

Admin: Port ``80`` (Docker) or Port ``8080`` (yarn)
Database: Port ``8081``
API: Port ``8010``
Trainer: Port ``8011``