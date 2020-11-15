## Boticot Trainer QuickStart

### Project setup

You should be in trainer folder and follow the next steps:

#### install dependencies
```
pip install rasa==1.10.0
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
To use your local environment varibales for development, you need to create a new file .env in the root of trainer folder.
Your local .env file will be ignored by git.