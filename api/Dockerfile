FROM python:3.6-slim

RUN pip install rasa==1.5.3
RUN pip install Tensorflow-datasets==1.3.0
RUN pip install Flask-PyMongo==2.3.0
RUN pip install flask==1.1.2
RUN pip install flask_cors==3.0.8
RUN pip install flask-compress==1.5.0
RUN pip install isodate==0.6.0
RUN pip install flask_jwt_extended==3.24.1
RUN pip install bcrypt==3.2.0
RUN pip install pytest==6.2.5
RUN pip install pytest-mock==3.6.1
RUN pip install gym==0.15.3

ADD . .

CMD ["python", "app.py"]