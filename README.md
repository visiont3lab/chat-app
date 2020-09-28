# chat-app

* Check the app at https://my-custom-chat-app.herokuapp.com/


```
virtualenv env
source env/bin/activate
pip install - r requirements.txt

# Python
python app.py

# Webserver
gunicorn -k eventlet  -w 1 --log-file=- app:app
```
