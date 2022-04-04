<img alt="Boticot" src="https://github.com/Boticot/boticot/blob/master/admin/src/assets/boticot.png"><br>

# Bot Interface and Conversational Toolkit

[![Release Date](https://img.shields.io/github/v/release/boticot/boticot)](https://github.com/boticot/boticot/releases)
[![Release Date](https://img.shields.io/github/release-date/boticot/boticot)](https://github.com/boticot/boticot/releases)

[![Contributors](https://img.shields.io/github/contributors-anon/boticot/boticot)](https://github.com/boticot/boticot/graphs/contributors)
[![License](https://img.shields.io/github/license/boticot/boticot)](https://github.com/boticot/boticot/blob/master/LICENSE)

## Boticot API QuickStart

### Project setup

You should be in api folder and follow the next steps:

#### install dependencies
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
```

#### Set up authentication configuration
Before running the project for the first time and for a security purpose, you should replace the default values of environment variables inside api:
* JWT_SECRET_KEY
* ADMIN_LOGIN
* ADMIN_PWD
The ADMIN_LOGIN and ADMIN_PWD will be used for authentication inside Boticot Admin

### Run project
```
flask run --port 8010
```

### Local Environment variables
To use your local environment variables for development, you need to create a new file .env in api folder and override default exisiting value in .flaskenv file.
Your local .env file will be ignored by git.


## Boticot Admin QuickStart

You should be in admin folder and follow the next steps:

### Prerequisite
Node 12

### Project setup
```
yarn install
```

#### Compiles and hot-reloads for development
```
yarn serve
```

## Boticot Trainer QuickStart

### Project setup

You should be in trainer folder and follow the next steps:

#### install dependencies
```
pip install rasa==1.5.3
pip install Tensorflow-datasets==1.3.0
pip install Flask-PyMongo==2.3.0
pip install flask==1.1.2
pip install flask_cors==3.0.8
pip install flask-compress==1.5.0
pip install isodate==0.6.0
```

### Run project
```
flask run --port 8011
```

### Local Environment variables
To use your local environment variables for development, you need to create a new file .env in trainer folder and override default exisiting value in .flaskenv file.
Your local .env file will be ignored by git.
