## Set environment

Under the project folder install the dependencies:

        $ source venv/bin/activate
        (venv)$ pip install -r requirements.txt

Requirements:
    
- Python3
- [venv](https://docs.python.org/3/library/venv.html)
- [pip](https://pypi.org/project/pip/)

## Create testing user

Running the next command, a form will be prompt to set user credentials for basic
authentication: 

        (venv) backend$ python createsuperuser

## Run project

        (venv) backend$ python manage.py runserver

And check project documentation [here](http://localhost:8000/api/docs)

You can be authenticated under [http://localhost:8000/api/v1/auth/login](http://localhost:8000/api/v1/auth/login)

## Run tests

Running tests

        (venv) backend$ python manage.py test

Get coverage details

        (venv) $ coverage run manage.py test
        (venv) $ coverage report
