## Boticot API QuickStart

#### Project setup

Recommended Python version: 3.6.8

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
Before running the project for the first time and for a security purpose, you should replace the default values of:
* JWT_SECRET_KEY
* ADMIN_LOGIN
* ADMIN_PWD
The ADMIN_LOGIN and ADMIN_PWD will be used for authentication inside Boticot Admin

#### Run API
```
flask run --port 8010
```
To launch tests, simply run ``pytest``. You can select a specific test file to run by appending it to the command.

### Local Environment variables
To use your local environment varibales for development, you need to create a new file .env in the root of api folder.
Your local .env file will be ignored by git.