# Starnavibook-api

> Simple API for some social network. Implemented with Django Rest Framework

[Here](https://starnavibook-api.herokuapp.com) you can find the deployed project

For aggregate likes on "../api/v1/analytics/" add `?date_fromYYYY-MM-DD&date_toYYYY-MM-DD` 
or `?date_fromYYYY-MM-DD` if you want to check likes to the present time

## Start project
* `git clone https://repo.url` - clone repo
* `virtualenv venv --python=/path/to/python` - configure virtual environment
* `pip install -r requirements.txt` - install requirements
* `create and configure .env file` - set secret settings (check **.env.example** here: ../config)
* `python manage.py migrate` - initiate db
* `python manage.py createsuperuser` - create superuser
* `python manage.py runserver` - run development server

For checking SQL-queries simply add `?debug-toolbar` after the url in your browser. You need to use "DEBUG ON" mode

## API endpoints

[Here](https://starnavibook-api.herokuapp.com/swagger/) you can find detail documentation (Swagger)