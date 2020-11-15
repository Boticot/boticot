## Boticot API QuickStart

### Project setup

You should be in api folder and follow the next steps:

#### install dependencies
```
pip install rasa==1.10.10
pip install Flask-PyMongo==2.3.0
pip install flask==1.1.2
pip install flask_cors==3.0.8
pip install flask-compress==1.5.0
pip install flask_jwt_extended==3.24.1
pip install isodate==0.6.0
pip install bcrypt==3.2.0
```

#### Set up authentication configuration
Before running the project for the first time and for a security purpose, you should replace the default values of:
* JWT_SECRET_KEY
* ADMIN_LOGIN
* ADMIN_PWD
The ADMIN_LOGIN and ADMIN_PWD will be used for authentication inside Boticot Admin

### Run project
```
flask run --port 8010
```

### Local Environment variables
To use your local environment varibales for development, you need to create a new file .env in the root of api folder.
Your local .env file will be ignored by git.