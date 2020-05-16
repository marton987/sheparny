# Code Challenge: Python/Django Developer @ SHERPANY

Home task project to build an "events" web application.

## Task description

Build an "events" web application where users can log in, create 
events and sign up for an event and withdraw from an event.

Any user can list events:

- Sorted so that upcoming events are first
- List view shows title, date and amount of participants
- List view shows the owner of the event (as the part of the email 
before the "@")
- Assume there will be many thousands of events, users and participants 
per event
- Any logged in user can create events
- Logged in user can edit own events
- Login with email and password
- Registration with email and password

### Out of scope

- email confirmation
- password reset
- change password
- profile editing
- change email

## Set environment

Under the project folder install the dependencies:

        $ cd backend/
        $ source venv/bin/activate
        (venv)$ pip install -r requirements.txt

Requirements:
    
- Python3
- [venv](https://docs.python.org/3/library/venv.html)
- [pip](https://pypi.org/project/pip/)

## Create testing user

Running the next command, a form will be prompt to set user credentials for basic
authentication: 

        (venv) django$ python createsuperuser

## Run project

        (venv) django$ python manage.py runserver

You can be authenticated under [http://localhost:8000/api/login](http://localhost:8000/api/login)
